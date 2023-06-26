import logging
from dataclasses import asdict
from typing import Dict

import backoff

import psycopg2
from psycopg2.errors import UndefinedTable
from psycopg2.extensions import connection
from psycopg2.extensions import cursor
from psycopg2.extras import DictCursor

logger = logging.getLogger(__name__)


class SaverError(Exception):
    """Кастомные исключения записи данных в postgres."""

    pass


class PostgresSaver:
    """Запись данных в Postgres."""

    def __init__(self, postgres_dsn: Dict):
        """Инициализация объекта для работы в postgres."""
        self.connection = self.postgres_connection(postgres_dsn)

    def __enter__(self) -> cursor:
        """Открытие коннекта к БД postgres."""
        logger.info('Calling __enter__')
        return self.connection.cursor()

    def __exit__(self, error: Exception, value: object, traceback: object) -> None:
        """Закрытие коннекта к БД postgres."""
        logger.info('Calling __exit__')
        self.connection.commit()
        self.connection.close()

    @backoff.on_exception(
        backoff.expo, Exception, logger=logger, max_value=10,
    )
    def postgres_connection(self, postgres_dsn: Dict) -> connection:
        """Подключение к Postgres."""
        return psycopg2.connect(**postgres_dsn, cursor_factory=DictCursor)

    def save_data(self, data_list, table_name: str, cursor: cursor):
        """Метод сохранения данных в БД postgres."""
        logger.info(f'start save {table_name}')
        logger.info(f'save {len(data_list)} records to {table_name}')
        try:
            for data in data_list:
                data = asdict(data)
                query = self._prepare_query(table_name, data)
                cursor.execute(query, data)
        except UndefinedTable as error:
            logger.critical(f'Table {table_name} does not exists in database! {error}')
            raise SaverError

    def _prepare_query(self, table_name: str, data):
        """Подготовка запроса вставки данных."""
        query = 'INSERT INTO {} '
        query = query.format(table_name)  # nosec
        query += '({0}) VALUES ({1}) ON CONFLICT (id) DO UPDATE SET {2}'

        fields = data.keys()
        columns = ', '.join(fields)
        values = ', '.join(['%({})s'.format(key) for key in fields])
        update = ', '.join(['{}=EXCLUDED.{}'.format(key, key) for key in fields if key != 'id'])
        query = query.format(columns, values, update)
        logger.debug(f'Prepared query: {query}')
        return query
