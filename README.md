# Вторая лабораторная работа — In-memory база данных

## Структура проекта
- src/db/__main__.py — точка входа
- src/db/tui.py — текстовый интерфейс
- src/db/backend/memory.py — реализация in-memory БД
- src/db/backend/exceptions.py — пользовательские исключения

## Функциональность
- Добавление записей (Create)
- Чтение с фильтрацией по полям (Read)
- Обновление записей по ID (Update)
- Удаление записей по ID (Delete)
- Обработка ошибок

## Запуск
bash
python3 -m src.db