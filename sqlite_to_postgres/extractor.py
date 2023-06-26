import logging
import sqlite3
from sqlite3 import Cursor, OperationalError
from typing import Generator

from sqlite_to_postgres.config import get_config

from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork

config = get_config()
logger = logging.getLogger(__name__)


class ExtractorError(Exception):
    """Кастомные исключения получения данных из sqlite."""

    pass


class SQLiteExtractor:
    """Извлечение данных из sqlite."""

    DEFAULT_LIMIT = 1000

    def __init__(self, file_name: str):
        """Инициализация объекта для работы в sqlite."""
        self.file_name = file_name
        self.connection = sqlite3.connect(self.file_name)
        self.connection.row_factory = self.dict_factory

    def dict_factory(self, cursor: Cursor, row):
        """Преобразование tuple полученного из БД в dict."""
        result = {}
        for idx, column in enumerate(cursor.description):
            result[column[0]] = row[idx]
        return result

    def __enter__(self):
        """Открытие коннекта к БД sqlite."""
        logger.info('Calling __enter__')
        return self.connection.cursor()

    def __exit__(self, error: Exception, value: object, traceback: object):
        """Закрытие коннекта к БД sqlite."""
        logger.info('Calling __exit__')
        self.connection.commit()
        self.connection.close()

    _MODEL_MAPPING = {
        'genre': Genre,
        'film_work': FilmWork,
        'genre_film_work': GenreFilmWork,
        'person': Person,
        'person_film_work': PersonFilmWork,
    }

    def extract_data(self, table_name: str, cursor: Cursor) -> Generator:
        """Метод выборки данных из sqlite пачками."""
        logger.info(f'start extract {table_name}')
        query = 'SELECT * FROM {}'
        query = query.format(table_name)  # nosec
        dto_class = self._MODEL_MAPPING[table_name]

        try:
            cursor.execute(query)
            while True:
                data = cursor.fetchmany(size=self.DEFAULT_LIMIT)
                if not data:
                    break
                logger.info(f'extract {len(data)} {table_name}')
                yield [dto_class.from_sqlite(**item) for item in data]
        except OperationalError as error:
            logger.critical(
                f'Some error while extract {table_name}: "{error}". '
                f'See in db {self.file_name}',
            )
            raise ExtractorError
