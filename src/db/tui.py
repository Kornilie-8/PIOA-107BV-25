# src/db/tui.py
from .backend.memory import InMemoryDatabase
from .backend.exceptions import RecordNotFoundError, RecordAlreadyExistsError, InvalidDataError

class TUI:
    def __init__(self):
        self.db = InMemoryDatabase()

    def _print_menu(self):
        print("\n=== База студентов (in-memory) ===")
        print("1. Добавить запись")
        print("2. Показать все записи")
        print("3. Найти записи по фильтру")
        print("4. Обновить запись (по id)")
        print("5. Удалить запись (по id)")
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

    def _print_records(self, records):
        if not records:
            print("Записи не найдены.")
            return
        for rec in records:
            print(rec)

    def _add_record(self):
        print("\nДобавление записи")
        student_id = self._read_int("id: ")
        first_name = input("first_name: ").strip()
        second_name = input("second_name: ").strip()
        age = self._read_int("age: ")
        sex = input("sex: ").strip()

        try:
            record = self.db.create_record(student_id, first_name, second_name, age, sex)
            print(f"Запись добавлена: {record}")
        except (InvalidDataError, RecordAlreadyExistsError) as e:
            print(f"Ошибка: {e}")

    def _show_all(self):
        print("\nСписок записей")
        self._print_records(self.db.select_records())

    def _find_records(self):
        print("\nПоиск по фильтру (Enter = пропустить поле)")
        filters = {}
        student_id = self._read_optional_int("student_id: ")
        if student_id is not None:
            filters["student_id"] = student_id

        first_name = input("first_name: ").strip()
        if first_name:
            filters["first_name"] = first_name

        second_name = input("second_name: ").strip()
        if second_name:
            filters["second_name"] = second_name

        age = self._read_optional_int("age: ")
        if age is not None:
            filters["age"] = age

        sex = input("sex: ").strip()
        if sex:
            filters["sex"] = sex

        result = self.db.select_records(**filters)
        self._print_records(result)

    def _update_record(self):
        print("\nОбновление записи")
        student_id = self._read_int("Введите id записи для обновления: ")
        print("Введите новые значения (Enter — оставить без изменений):")
        updates = {}
        first_name = input("first_name: ").strip()
        if first_name:
            updates["first_name"] = first_name
        second_name = input("second_name: ").strip()
        if second_name:
            updates["second_name"] = second_name
        age_str = input("age: ").strip()
        if age_str:
            try:
                updates["age"] = int(age_str)
            except ValueError:
                print("Возраст должен быть целым числом, поле не будет обновлено.")
        sex = input("sex: ").strip()
        if sex:
            updates["sex"] = sex

        if not updates:
            print("Нет полей для обновления.")
            return

        try:
            updated = self.db.update_record(student_id, **updates)
            print(f"Запись обновлена: {updated}")
        except RecordNotFoundError as e:
            print(f"Ошибка: {e}")
        except InvalidDataError as e:
            print(f"Ошибка: {e}")

    def _delete_record(self):
        print("\nУдаление записи")
        student_id = self._read_int("Введите id записи для удаления: ")
        try:
            deleted = self.db.delete_record(student_id)
            print(f"Запись удалена: {deleted}")
        except RecordNotFoundError as e:
            print(f"Ошибка: {e}")

    def run(self):
        while True:
            self._print_menu()
            choice = input("Выберите действие: ").strip()
            if choice == "1":
                self._add_record()
            elif choice == "2":
                self._show_all()
            elif choice == "3":
                self._find_records()
            elif choice == "4":
                self._update_record()
            elif choice == "5":
                self._delete_record()
            elif choice == "0":
                print("Выход из программы.")
                break
            else:
                print("Неизвестная команда.")