"""
withenv ./.env poetry run python3 ./src/script/sqlite_to_postgres/load_data.py
"""

import asyncio

from script.sqlite_to_postgres.etl_movies.settings import Settings
from script.sqlite_to_postgres.etl_movies.postgres_saver import PostgresSaver
from script.sqlite_to_postgres.etl_movies.sqlite_loader import SQLiteLoader
from script.sqlite_to_postgres.etl_movies.dto.film_work import FilmWorkDTO, GenreDTO, GenreFilmWorkDTO, PersonDTO

# FIXME: что-то более структурированное что-ли
table_dto_map = {
    'film_work': FilmWorkDTO,
    'person': PersonDTO,
    'genre': GenreDTO,
    'genre_film_work': GenreFilmWorkDTO,
}


async def load_from_sqlite():
    """Основной метод загрузки данных из SQLite в Postgres"""
    settings = Settings()
    postgres_saver = PostgresSaver(settings)
    sqlite_loader = SQLiteLoader(settings)

    async with sqlite_loader, postgres_saver:
        for table, dto in table_dto_map.items():
            data = await sqlite_loader.extract(table, dto)
            await postgres_saver.load_data(data=data, db_table=table, dto_class=dto)

    # data = sqlite_loader.load_movies()
    # postgres_saver.save_all_data(data)


if __name__ == '__main__':
    asyncio.run(load_from_sqlite())
    # dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    # with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg.connect(
    #     **dsl, row_factory=dict_row, cursor_factory=ClientCursor
    # ) as pg_conn:
    #     load_from_sqlite(sqlite_conn, pg_conn)
