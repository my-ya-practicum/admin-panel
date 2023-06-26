import logging
import logging.config

from sqlite_to_postgres.config import get_config

from extractor import ExtractorError, SQLiteExtractor

from saver import PostgresSaver, SaverError


def load_from_sqlite():
    """Основной метод загрузки данных из SQLite в Postgres."""
    config = get_config()
    logger = logging.getLogger(__name__)
    logging.config.dictConfig(config.LOGGING)

    postgres_saver = PostgresSaver(postgres_dsn=config.postgres_dsn)
    sqlite_extractor = SQLiteExtractor(file_name=config.SQLITE_PATH)

    with sqlite_extractor as sqlite_cursor, postgres_saver as postgres_cursor:
        try:
            # 1. film_work
            for film_work in sqlite_extractor.extract_data('film_work', cursor=sqlite_cursor):
                postgres_saver.save_data(film_work, 'content.film_work', postgres_cursor)

            # 2. genre
            for genre in sqlite_extractor.extract_data('genre', cursor=sqlite_cursor):
                postgres_saver.save_data(genre, 'content.genre', postgres_cursor)

            # 3. genre_film_work
            for genre_film_work in sqlite_extractor.extract_data(
                'genre_film_work', cursor=sqlite_cursor,
            ):
                postgres_saver.save_data(genre_film_work, 'content.genre_film_work', postgres_cursor)

            # 4. person
            for person in sqlite_extractor.extract_data('person', cursor=sqlite_cursor):
                postgres_saver.save_data(person, 'content.person', postgres_cursor)

            # 5. person_film_work
            for person_film_work in sqlite_extractor.extract_data(
                'person_film_work', cursor=sqlite_cursor,
            ):
                postgres_saver.save_data(person_film_work, 'content.person_film_work', postgres_cursor)

        except (ExtractorError, SaverError) as error:
            logger.error(error)


if __name__ == '__main__':
    load_from_sqlite()
