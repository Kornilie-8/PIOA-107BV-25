import unittest

from src.db.backend.errors import (
    TableAlreadyExistsError,
    TableNotFoundError,
    MissingColumnError,
    UnknownColumnError,
)
from src.db.backend.memory import MemoryDatabase


class TestMemoryDatabase(unittest.TestCase):
    def setUp(self):
        self.db = MemoryDatabase()

    def test_create_table(self):
        self.db.create_table("students", ("student_id", "first_name", "age"))
        self.assertTrue(self.db._table_exists("students"))

    def test_create_duplicate_table(self):
        self.db.create_table("students", ("student_id", "first_name", "age"))
        with self.assertRaises(TableAlreadyExistsError):
            self.db.create_table("students", ("student_id", "first_name", "age"))

    def test_insert_and_select(self):
        self.db.create_table("students", ("student_id", "first_name", "age"))
        self.db.insert_record("students", {"student_id": 1, "first_name": "Иван", "age": 20})
        records = self.db.select_records("students")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["first_name"], "Иван")

    def test_select_with_filter(self):
        self.db.create_table("students", ("student_id", "first_name", "age"))
        self.db.insert_record("students", {"student_id": 1, "first_name": "Иван", "age": 20})
        self.db.insert_record("students", {"student_id": 2, "first_name": "Мария", "age": 22})
        records = self.db.select_records("students", first_name="Мария")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["student_id"], 2)

    def test_insert_missing_column(self):
        self.db.create_table("students", ("student_id", "first_name", "age"))
        with self.assertRaises(MissingColumnError):
            self.db.insert_record("students", {"student_id": 1, "first_name": "Иван"})

    def test_insert_unknown_column(self):
        self.db.create_table("students", ("student_id", "first_name", "age"))
        with self.assertRaises(UnknownColumnError):
            self.db.insert_record("students", {"student_id": 1, "first_name": "Иван", "age": 20, "sex": "M"})

    def test_select_from_missing_table(self):
        with self.assertRaises(TableNotFoundError):
            self.db.select_records("missing")

    def test_insert_into_missing_table(self):
        with self.assertRaises(TableNotFoundError):
            self.db.insert_record("missing", {"student_id": 1, "first_name": "Иван", "age": 20})


if __name__ == "main":
    unittest.main()