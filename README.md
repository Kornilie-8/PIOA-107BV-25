# Четвёртая лабораторная работа — Файловая СУБД

## Структура проекта
PIOA-НомерГруппы/
├── src/
│   └── db/
│       ├── backend/
│       │   ├── init.py
│       │   ├── database.py    — абстрактный интерфейс БД
│       │   ├── errors.py      — пользовательские исключения
│       │   ├── file.py        — файловая реализация (JSON)
│       │   ├── memory.py      — in-memory реализация
│       │   └── table.py       — класс таблицы
│       ├── init.py
│       ├── main.py        — точка входа
│       └── tui.py             — текстовый интерфейс
├── data/                      — файлы таблиц (JSON)
├── tests/
│   ├── init.py
│   ├── test_memory.py         — тесты in-memory БД
│   └── test_file_database.py  — тесты файловой БД
└── README.md
## Функциональность

- Создание таблиц с произвольным набором колонок
- Добавление записей (Create)
- Чтение с фильтрацией (Read)
- Две реализации: in-memory (MemoryDatabase) и файловая (FileDatabase в JSON)
- Единый интерфейс через абстрактный класс Database
- Обработка ошибок через пользовательские исключения
- Покрытие тестами (unittest + pytest)

## Различия между in-memory и файловой реализациями

| Характеристика | MemoryDatabase | FileDatabase |
|---|---|---|
| Хранение | в оперативной памяти | в JSON-файлах на диске |
| Сохранение между запусками | нет | да |
| Формат | словарь Python | JSON |
| Быстродействие | быстрее | медленнее |

## Запуск
bash
python3 -m src.db
Запуск тестов
bash
python3 -m pytest tests/ -v

Затем коммит и пуш:
git add -A
git commit -m "Task 4: file database with JSON, tests"
git push origin task4
