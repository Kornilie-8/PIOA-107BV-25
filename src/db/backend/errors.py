# src/db/backend/exceptions.py
"""Пользовательские исключения для базы данных."""

class DatabaseError(Exception):
    """Базовое исключение для всех ошибок БД."""
    pass

class RecordNotFoundError(DatabaseError):
    """Запись с указанём id не найдена."""
    pass

class RecordAlreadyExistsError(DatabaseError):
    """Запись с таким id уже существует."""
    pass

class InvalidDataError(DatabaseError):
    """Некорректные данные (например, отрицательный возраст)."""
    pass

"""Пользовательские исключения для базы данных."""


class DatabaseError(Exception):
    """Базовый класс для ошибок базы данных."""


class TableAlreadyExistsError(DatabaseError):
    """Ошибка, возникающая при попытке создать уже существующую таблицу."""


class TableNotFoundError(DatabaseError):
    """Ошибка, возникающая при обращении к несуществующей таблице."""


class MissingColumnError(DatabaseError):
    """Ошибка, возникающая при отсутствии обязательного поля в записи."""


class UnknownColumnError(DatabaseError):
    """Ошибка, возникающая при использовании поля, которого нет в схеме таблицы."""


class InvalidStorageDataError(DatabaseError):
    """Ошибка, возникающая при чтении повреждённых данных из файла."""