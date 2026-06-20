# src/db/backend/memory.py
from .exceptions import RecordNotFoundError, RecordAlreadyExistsError, InvalidDataError

class InMemoryDatabase:
    def __init__(self):
        self._data: dict[int, dict] = {}
        self._columns = ("student_id", "first_name", "second_name", "age", "sex")

    def create_record(self, student_id: int, first_name: str, second_name: str,
                      age: int, sex: str) -> dict:
        if age < 0:
            raise InvalidDataError("Возраст не может быть отрицательным.")
        if student_id in self._data:
            raise RecordAlreadyExistsError(f"Запись с id={student_id} уже существует.")

        first_name = first_name.strip()
        second_name = second_name.strip()
        sex = sex.strip()

        record = {
            "student_id": student_id,
            "first_name": first_name,
            "second_name": second_name,
            "age": age,
            "sex": sex,
        }
        self._data[student_id] = record
        return record.copy()

    def select_records(self, **filters) -> list[dict]:
        if not filters:
            return [rec.copy() for rec in self._data.values()]

        result = []
        for record in self._data.values():
            match = True
            for key, value in filters.items():
                if record.get(key) != value:
                    match = False
                    break
            if match:
                result.append(record.copy())
        return result

    def update_record(self, student_id: int, **updates) -> dict:
        if student_id not in self._data:
            raise RecordNotFoundError(f"Запись с id={student_id} не найдена.")

        record = self._data[student_id]
        for key, value in updates.items():
            if key == "age" and value < 0:
                raise InvalidDataError("Возраст не может быть отрицательным.")
            if key in self._columns:
                if key in ("first_name", "second_name", "sex") and isinstance(value, str):
                    record[key] = value.strip()
                else:
                    record[key] = value
        return record.copy()

    def delete_record(self, student_id: int) -> dict:
        if student_id not in self._data:
            raise RecordNotFoundError(f"Запись с id={student_id} не найдена.")
        deleted = self._data.pop(student_id)
        return deleted.copy()