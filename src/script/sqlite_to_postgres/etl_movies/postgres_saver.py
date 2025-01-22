from dataclasses import fields
from itertools import repeat
import logging.config
import psycopg

from types import TracebackType
from typing import Any, AsyncGenerator, Generator, Optional, Type

from script.sqlite_to_postgres.etl_movies.dto.base import DataClass
from script.sqlite_to_postgres.etl_movies.dto.film_work import FilmWorkDTO
from script.sqlite_to_postgres.etl_movies.logger import LOGGING_CONFIG
from script.sqlite_to_postgres.etl_movies.settings import Settings

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class PostgresSaver:
    def __init__(self, settings: Settings):
        self.content_schema = 'content'
        self.chunk_size = settings.postgres_config.load_chunk_size
        self.connection = self.postgres_connect(settings.postgres_config.database_url)

    def postgres_connect(self, postgres_dns: str):
        return psycopg.connect(postgres_dns)

    async def __aenter__(self):
        logger.debug('Calling __aenter__')
        self.cursor = self.connection.cursor()
        return self.cursor

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        logger.debug('Calling __aexit__')
        # self.connection.commit()
        self.connection.close()

    async def load_data(
        self,
        db_table: str,
        dto_class: Type[DataClass],
        data: AsyncGenerator[Generator[FilmWorkDTO, None, None], Any],
    ):
        await self._build_query(
            db_table=db_table,
            dto_class=dto_class,
            data=data,
        )

    async def _build_query(
        self,
        data: AsyncGenerator[Generator[FilmWorkDTO, None, None], Any],
        db_table: str,
        dto_class: Type[DataClass],
    ):
        field_names = [field.name for field in fields(dto_class)]
        base_query = f"INSERT INTO {self.content_schema}.{db_table} ({", ".join(field_names)}) VALUES "
        placeholder = ", ".join(repeat('%s', len(field_names)))
        async for list_items in data:
            count_items = 0
            values = list()
            for item in list_items:
                count_items += 1
                for field in fields(dto_class):
                    values.append(getattr(item, field.name))
            placeholders = ', '.join(f"({placeholder})" for _ in range(count_items))
            update = ', '.join(['{}=EXCLUDED.{}'.format(key, key) for key in field_names if key != 'id'])
            on_conflict = f"ON CONFLICT (id) DO UPDATE SET {update}"
            query = f"{base_query} {placeholders} {on_conflict}"
            await self._execute_query(query, values)

    async def _execute_query(self, query: str, data: list[Any]):
        logger.debug(f"execute: {query}")
        self.cursor.execute(query, data)
        self.connection.commit()
