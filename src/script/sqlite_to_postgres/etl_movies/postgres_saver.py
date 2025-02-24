from dataclasses import fields
import logging.config
import psycopg

from types import TracebackType
from typing import Any, AsyncGenerator, Generator, Optional, Type

from script.sqlite_to_postgres.etl_movies.dto.base import DataClass
from script.sqlite_to_postgres.etl_movies.dto.film_work import (
    FilmWorkDTO,
    GenreDTO,
    GenreFilmWorkDTO,
    PersonDTO,
    PersonFilmWorkDTO,
)
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
        self.connection.close()

    async def load_data(
        self,
        db_table: str,
        dto_class: Type[DataClass],
        data: AsyncGenerator[
            Generator[FilmWorkDTO | PersonDTO | GenreDTO | GenreFilmWorkDTO | PersonFilmWorkDTO, None, None], Any
        ],
    ):
        """
        Асинхронный метод для загрузки данных в таблицу базы данных с обработкой конфликтов.

        Описание:
        Метод load_data выполняет массовую вставку данных в указанную таблицу базы данных,
        используя предоставленные данные и класс DTO (Data Transfer Object).
        При возникновении конфликта по уникальному полю id, данные обновляются с помощью конструкции ON CONFLICT.

        Параметры:
        - db_table: Название таблицы в базе данных, куда будут вставлены данные.
        - dto_class: Класс DTO, описывающий структуру данных. Должен быть совместим с типами данных из параметра data.
        - data: Асинхронный генератор, предоставляющий порции данных для вставки.
                Каждая порция представляет собой последовательность объектов DTO.

        Логика работы:
        1. **Подготовка запроса**:
        - Извлекаются имена полей из класса DTO (field_names).
        - Формируется базовая часть SQL-запроса для вставки данных (INSERT INTO).

        2. **Обработка данных**:
        - Для каждой порции данных (list_items) из асинхронного генератора data:
            - Собираются значения всех полей для каждого объекта DTO.
            - Формируются плейсхолдеры (placeholders) для параметров вставки.

        3. **Обработка конфликтов**:
        - Если происходит конфликт по полю id,
          выполняется обновление остальных полей с использованием значений из EXCLUDED.

        4. **Выполнение запроса**:
        - Сформированный SQL-запрос передается в метод _execute_query для выполнения.
        """
        field_names = [field.name for field in fields(dto_class)]
        base_query = f"INSERT INTO {self.content_schema}.{db_table} ({", ".join(field_names)}) VALUES "
        placeholder = ", ".join(['%s'] * len(field_names))
        async for list_items in data:
            values = list()
            item_count = 0
            for item in list_items:
                item_count += 1
                values.extend([getattr(item, field) for field in field_names])
            placeholders = ', '.join(f"({placeholder})" for _ in range(item_count))
            update = ', '.join(['{}=EXCLUDED.{}'.format(key, key) for key in field_names if key != 'id'])
            on_conflict = f"ON CONFLICT (id) DO UPDATE SET {update}"
            query = f"{base_query} {placeholders} {on_conflict}"
            await self._execute_query(query, values)

    async def _execute_query(self, query: str, data: list[Any]):
        logger.debug(f"execute: {query}")
        logger.debug(f"data: {data}")
        self.cursor.execute(query, data)  # type: ignore
        self.connection.commit()
