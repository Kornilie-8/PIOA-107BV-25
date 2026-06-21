# src/db/tui.py
from .backend.file import FileDatabase
from .backend.csv_db import CSVDatabase
from .backend.memory import MemoryDatabase
from .backend.errors import (
    TableAlreadyExistsError,
    TableNotFoundError,
    MissingColumnError,
    UnknownColumnError,
)


class TUI:
    def __init__(self) -> None:
        print("Выберите тип базы данных:")
        print("1. In-memory")
        print("2. File database (JSON)")
        print("3. File database (CSV)")

        choice = input("Введите номер: ").strip()
        if choice == "2":
            self.db = FileDatabase()
        elif choice == "3":
            self.db = CSVDatabase()
        else:
            self.db = MemoryDatabase()

        self._current_table: str | None = None

    def _print_menu(self) -> None:
        print(f"\n=== База данных (таблица: {self._current_table or 'не выбрана'}) ===")
        print("1. Создать таблицу")
        print("2. Добавить запись")
        print("3. Показать все записи")
        print("4. Найти записи по фильтру")
        print("0. Выход")

    def _read_int(self, prompt: str) -> int:
        while True:
            raw = input(prompt).strip()
            try:
                return int(raw)
            except ValueError:
                print("Ошибка: введите целое число.")

    def _read_optional_int(self, prompt: str) -> int | None:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число или оставьте поле пустым.")
            return None

    def _print_records(self, records: list[dict]) -> None:
        if not records:
            print("Записи не найдены.")
            return
        for rec in records:
            print(rec)

    def _create_table(self) -> None:
        print("\nСоздание таблицы")
        table_name = input("Название таблицы: ").strip()
        if not table_name:
            print("Ошибка: название не может быть пустым.")
            return

        columns_str = input("Колонки через запятую (например: student_id, first_name, age): ").strip()
        if not columns_str:
            print("Ошибка: нужна хотя бы одна колонка.")
            return

        columns = tuple(col.strip() for col in columns_str.split(",") if col.strip())

        try:
            self.db.create_table(table_name, columns)
            self._current_table = table_name
            print(f"Таблица '{table_name}' создана.")
        except TableAlreadyExistsError as e:
            print(f"Ошибка: {e}")

    def _add_record(self) -> None:
        if self._current_table is None:
            print("Сначала создайте таблицу.")
            return

        print(f"\nДобавление записи в '{self._current_table}'")
        record = {}
        columns = self._get_columns()

        for col in columns:
            value = input(f"{col}: ").strip()
            if col in ("student_id", "age"):
                try:
                    value = int(value)
                except ValueError:
                    print(f"Ошибка: поле '{col}' должно быть числом.")
                    return
            record[col] = value

        try:
            self.db.insert_record(self._current_table, record)
            print(f"Запись добавлена.")
        except (MissingColumnError, UnknownColumnError) as e:
            print(f"Ошибка: {e}")

    def _get_columns(self) -> tuple:
        try:
            table = self.db._load_table(self._current_table)
            return table.columns
        except TableNotFoundError:
            return ()

    def _show_all(self) -> None:
        if self._current_table is None:
            print("Сначала создайте таблицу.")
            return

        print(f"\nСписок записей '{self._current_table}'")
        try:
            self._print_records(self.db.select_records(self._current_table))
        except TableNotFoundError as e:
            print(f"Ошибка: {e}")

    def _find_records(self) -> None:
        if self._current_table is None:
            print("Сначала создайте таблицу.")
            return
        print(f"\nПоиск по фильтру в '{self._current_table}' (Enter = пропустить)")
        filters = {}
        for col in self._get_columns():
            value = input(f"{col}: ").strip()
            if value:
                if col in ("student_id", "age"):
                    try:
                        value = int(value)
                    except ValueError:
                        print(f"Ошибка: поле '{col}' должно быть числом.")
                        return
                filters[col] = value

        try:
            result = self.db.select_records(self._current_table, **filters)
            self._print_records(result)
        except (TableNotFoundError, UnknownColumnError) as e:
            print(f"Ошибка: {e}")

    def run(self) -> None:
        while True:
            self._print_menu()
            choice = input("Выберите действие: ").strip()
            if choice == "1":
                self._create_table()
            elif choice == "2":
                self._add_record()
            elif choice == "3":
                self._show_all()
            elif choice == "4":
                self._find_records()
            elif choice == "0":
                print("Выход из программы.")
                break
            else:
                print("Неизвестная команда.")