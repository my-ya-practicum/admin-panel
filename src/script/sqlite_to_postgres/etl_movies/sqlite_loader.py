from dataclasses import fields
import sqlite3
import logging
import logging.config

from types import TracebackType
from typing import Optional, Type
from script.sqlite_to_postgres.etl_movies.dto.base import DataClass
from script.sqlite_to_postgres.etl_movies.dto.film_work import FilmWorkDTO
from script.sqlite_to_postgres.etl_movies.logger import LOGGING_CONFIG
from script.sqlite_to_postgres.etl_movies.settings import Settings


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# FIXME: что-то более структурированное что-ли
table_dto_map = {
    'film_work': FilmWorkDTO,
}


class SQLiteLoader:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.chunk_size = settings.sqlite_config.extract_chunk_size

    async def __aenter__(self):
        db_file_path = self.settings.sqlite_config.sqlite_db_file_path
        logger.info(f"Try connect to {db_file_path}")
        self.connect = sqlite3.connect(db_file_path)
        self.connect.row_factory = sqlite3.Row
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        pass

    async def extract(self):
        for table, dto in table_dto_map.items():
            return await self._build_query(db_table=table, dto_class=dto), table, dto

    async def _build_query(self, db_table: str, dto_class: Type[DataClass]):
        field_names = [field.name for field in fields(dto_class)]
        query = f"SELECT {", ".join(field_names)} "
        query += f"FROM {db_table} "
        return self._execute_query(query, dto_class)

    async def _execute_query(self, query: str, dto_class: Type[DataClass]):
        cursor = self.connect.cursor()
        logger.debug(f"execute: {query}")
        cursor.execute(query)
        while rows_chunk := cursor.fetchmany(self.chunk_size):
            yield (dto_class(**dict(row)) for row in rows_chunk)
