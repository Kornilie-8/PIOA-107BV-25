import csv
from pathlib import Path

from .database import Database
from .errors import InvalidStorageDataError, TableNotFoundError
from .table import Table


class CSVDatabase(Database):
    """База данных, которая хранит таблицы в CSV-файлах."""

    def __init__(self, directory: str = "data") -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _table_exists(self, table_name: str) -> bool:
        return self._get_table_path(table_name).exists()

    def _load_table(self, table_name: str) -> Table:
        table_path = self._get_table_path(table_name)
        if not table_path.exists():
            raise TableNotFoundError(
                f"Таблица '{table_name}' не существует."
            )

        try:
            with table_path.open("r", encoding="utf-8", newline="") as file:
                reader = csv.DictReader(file)
                columns = tuple(reader.fieldnames) if reader.fieldnames else ()
                records = list(reader)
        except (csv.Error, UnicodeDecodeError) as error:
            raise InvalidStorageDataError(
                "Файл таблицы содержит некорректные данные CSV."
            ) from error

        return Table(columns, records)

    def _save_table(self, table_name: str, table: Table) -> None:
        table_path = self._get_table_path(table_name)

        with table_path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=list(table.columns))
            writer.writeheader()
            writer.writerows(table.records)

    def _get_table_path(self, table_name: str) -> Path:
        return self.directory / f"{table_name}.csv"