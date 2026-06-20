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