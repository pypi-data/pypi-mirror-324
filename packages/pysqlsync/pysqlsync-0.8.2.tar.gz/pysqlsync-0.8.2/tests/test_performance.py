import dataclasses
import os.path
import unittest

from tsv.helper import Generator, Parser

import tests.model.event
from pysqlsync.base import GeneratorOptions
from pysqlsync.data.generator import random_objects
from pysqlsync.formation.py_to_sql import EnumMode
from pysqlsync.model.id_types import LocalId
from pysqlsync.model.properties import get_class_properties
from tests.measure import Timer
from tests.model.event import EventRecord
from tests.params import (
    MSSQLBase,
    MySQLBase,
    PostgreSQLBase,
    TestEngineBase,
    configure,
    has_env_var,
)

if __name__ == "__main__":
    configure()


def generate_input_file(data_file_path: str, record_count: int) -> None:
    "Generates data and writes a file to be used as input for performance testing."

    generator = Generator()
    items = random_objects(EventRecord, record_count)
    with open(data_file_path, "wb") as f:
        generator.generate_file(f, (dataclasses.astuple(item) for item in items))


@unittest.skipUnless(has_env_var("INTEGRATION"), "database tests are disabled")
class TestPerformance(TestEngineBase, unittest.IsolatedAsyncioTestCase):
    RECORD_COUNT = 100000

    @property
    def options(self) -> GeneratorOptions:
        return GeneratorOptions(
            enum_mode=EnumMode.RELATION,
            namespaces={tests.model.event: "performance_test"},
        )

    @classmethod
    def setUpClass(cls) -> None:
        data_file_path = os.path.join(os.path.dirname(__file__), "performance_test.tsv")
        if not os.path.exists(data_file_path):
            generate_input_file(data_file_path, cls.RECORD_COUNT)

    async def asyncSetUp(self) -> None:
        async with self.engine.create_connection(self.parameters, self.options) as conn:
            await conn.drop_schema(LocalId("performance_test"))

    async def test_rows_upsert(self) -> None:
        async with self.engine.create_connection(self.parameters, self.options) as conn:
            await conn.create_objects([EventRecord])

            table = conn.get_table(EventRecord)
            column_types = get_class_properties(EventRecord).tsv_types
            parser = Parser(column_types)

            with Timer("read file"):
                with open(
                    os.path.join(os.path.dirname(__file__), "performance_test.tsv"),
                    "rb",
                ) as f:
                    data = parser.parse_file(f)

            with Timer(f"insert into {self.engine.name} database table"):
                await conn.insert_rows(table, field_types=column_types, records=data)

            self.assertEqual(
                await conn.query_one(int, f"SELECT COUNT(*) FROM {table.name};"),
                len(data),
            )

            await conn.drop_objects()


@unittest.skipUnless(has_env_var("POSTGRESQL"), "PostgreSQL tests are disabled")
class TestPostgreSQLConnection(PostgreSQLBase, TestPerformance):
    pass


@unittest.skipUnless(has_env_var("MSSQL"), "Microsoft SQL tests are disabled")
class TestMSSQLConnection(MSSQLBase, TestPerformance):
    pass


@unittest.skipUnless(has_env_var("MYSQL"), "MySQL tests are disabled")
class TestMySQLConnection(MySQLBase, TestPerformance):
    pass


del TestPerformance

if __name__ == "__main__":
    unittest.main()
