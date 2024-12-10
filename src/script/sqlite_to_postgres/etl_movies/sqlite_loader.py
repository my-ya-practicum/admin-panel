import sqlite3
import logging
import logging.config
from enum import StrEnum, auto

from types import TracebackType
from typing import Optional, Type
from script.sqlite_to_postgres.etl_movies.logger import LOGGING_CONFIG
from script.sqlite_to_postgres.etl_movies.settings import Settings


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class TablesEnum(StrEnum):
    film_work = auto()


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
        return await self._build_query(db_table=TablesEnum.film_work)

    async def _build_query(self, db_table: TablesEnum):
        query = f"SELECT id, title "
        query += f"FROM {db_table.name} "
        return self._execute_query(query)

    async def _execute_query(self, query: str):
        cursor = self.connect.cursor()
        # # while rows_chunk := cursor.execute(query).fetchmany(self.chunk_size):
        while row := cursor.execute(query).fetchone():
            yield dict(row)
        #     # yield [dict(row) for row in rows_chunk]
