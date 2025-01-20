from dataclasses import fields
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
        self.settings = settings
        self.connection = self.postgres_connect(settings.postgres_config.database_url)

    def postgres_connect(self, postgres_dns: str):
        return psycopg.connect(postgres_dns)

    async def __aenter__(self):
        logger.debug('Calling __aenter__')
        return self.connection.cursor()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        logger.debug('Calling __aexit__')

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

        async for i in data:
            for j in i:
                logger.debug(j)

    async def _build_query(
        self,
        db_table: str,
        dto_class: Type[DataClass],
        data: AsyncGenerator[Generator[FilmWorkDTO, None, None], Any],
    ):
        field_names = [field.name for field in fields(dto_class)]
        query = f"INSERT INTO {self.content_schema}.{db_table} ({", ".join(field_names)}) VALUES "
        logger.debug(query)
        # query += f""
        # return self._execute_query(query, dto_class)
