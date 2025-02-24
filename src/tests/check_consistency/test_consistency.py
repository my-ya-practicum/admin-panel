import sqlite3
import psycopg


# from script.sqlite_to_postgres.etl_movies.dto.film_work import FilmWorkDTO, GenreDTO, GenreFilmWorkDTO, PersonDTO


class TestIntegrityData:
    """Проверка целостности данных."""

    def test_count_film_works(
        self,
        pg_connect: psycopg.Connection,
        sqlite3_connect: sqlite3.Connection,
    ):
        """Проверка кол-ва записей film_work."""
        sqlite3_cursor = sqlite3_connect.cursor()
        query_template = """SELECT count(1) FROM {0}"""
        count_film_works = sqlite3_cursor.execute(query_template.format('film_work'))
        [sqlite3_rows] = count_film_works.fetchone()

        pg_cursor = pg_connect.cursor()
        pg_cursor.execute(query_template.format('"content"."film_work"'))
        (pg_rows) = pg_cursor.fetchone()

        assert sqlite3_rows == pg_rows[0]  # type: ignore

    def test_count_genre(
        self,
        pg_connect: psycopg.Connection,
        sqlite3_connect: sqlite3.Connection,
    ):
        """Проверка кол-ва записей genre."""
        sqlite3_cursor = sqlite3_connect.cursor()
        query_template = """SELECT count(1) FROM {0}"""
        count_genres = sqlite3_cursor.execute(query_template.format('genre'))
        [sqlite3_rows] = count_genres.fetchone()

        pg_cursor = pg_connect.cursor()
        pg_cursor.execute(query_template.format('"content"."genre"'))
        (pg_rows) = pg_cursor.fetchone()

        assert sqlite3_rows == pg_rows[0]  # type: ignore

    def test_count_person(
        self,
        pg_connect: psycopg.Connection,
        sqlite3_connect: sqlite3.Connection,
    ):
        """Проверка кол-ва записей person."""
        sqlite3_cursor = sqlite3_connect.cursor()
        query_template = """SELECT count(1) FROM {0}"""
        count_persons = sqlite3_cursor.execute(query_template.format('person'))
        [sqlite3_rows] = count_persons.fetchone()

        pg_cursor = pg_connect.cursor()
        pg_cursor.execute(query_template.format('"content"."person"'))
        (pg_rows) = pg_cursor.fetchone()

        assert sqlite3_rows == pg_rows[0]  # type: ignore

    def test_count_genre_film_work(
        self,
        pg_connect: psycopg.Connection,
        sqlite3_connect: sqlite3.Connection,
    ):
        """Проверка кол-ва записей genre_film_work."""
        sqlite3_cursor = sqlite3_connect.cursor()
        query_template = """SELECT count(1) FROM {0}"""
        count_genre_film_works = sqlite3_cursor.execute(query_template.format('genre_film_work'))
        [sqlite3_rows] = count_genre_film_works.fetchone()

        pg_cursor = pg_connect.cursor()
        pg_cursor.execute(query_template.format('"content"."genre_film_work"'))
        (pg_rows) = pg_cursor.fetchone()

        assert sqlite3_rows == pg_rows[0]  # type: ignore

    def test_count_person_film_work(
        self,
        pg_connect: psycopg.Connection,
        sqlite3_connect: sqlite3.Connection,
    ):
        """Проверка кол-ва записей person_film_work."""
        sqlite3_cursor = sqlite3_connect.cursor()
        query_template = """SELECT count(1) FROM {0}"""
        count_person_film_work = sqlite3_cursor.execute(query_template.format('person_film_work'))
        [sqlite3_rows] = count_person_film_work.fetchone()

        pg_cursor = pg_connect.cursor()
        pg_cursor.execute(query_template.format('"content"."person_film_work"'))
        (pg_rows) = pg_cursor.fetchone()

        assert sqlite3_rows == pg_rows[0]  # type: ignore


# class TestContent:
#     """Проверка содержимого записей."""

#     def test_film_work_records(
#         self,
#         pg_connect: connection,
#         sqlite3_connect: Connection,
#     ):
#         """Проверка записей film_work."""
#         sqlite3_cursor = sqlite3_connect.cursor()
#         pg_cursor = pg_connect.cursor()

#         sqlite3_query = """
#             SELECT "created_at", "updated_at", "id", "title", "description", "creation_date"
#             FROM film_work
#         """
#         sqlite3_rows = sqlite3_cursor.execute(sqlite3_query)

#         pg_query = """
#             SELECT "created", "modified", "id", "title", "description", "creation_date"
#             FROM "content"."film_work" WHERE id = '{0}'
#         """

#         for row in sqlite3_rows.fetchall():
#             sqlite3_data = FilmWork(*row)
#             pg_cursor.execute(pg_query.format(sqlite3_data.id))
#             pg_data = FilmWork(*pg_cursor.fetchone())
#             assert sqlite3_data == pg_data

#     def test_genre_records(
#         self,
#         pg_connect: connection,
#         sqlite3_connect: Connection,
#     ):
#         """Проверка записей genre."""
#         sqlite3_cursor = sqlite3_connect.cursor()
#         pg_cursor = pg_connect.cursor()

#         sqlite3_query = """
#             SELECT "created_at", "updated_at", "id", "name", "description"
#             FROM genre
#         """
#         sqlite3_rows = sqlite3_cursor.execute(sqlite3_query)

#         pg_query = """
#             SELECT "created", "modified", "id", "name", "description"
#             FROM "content"."genre" WHERE id = '{0}'
#         """

#         for row in sqlite3_rows.fetchall():
#             sqlite3_data = Genre(*row)
#             pg_cursor.execute(pg_query.format(sqlite3_data.id))
#             pg_data = Genre(*pg_cursor.fetchone())
#             assert sqlite3_data == pg_data

#     def test_genre_film_work_records(
#         self,
#         pg_connect: connection,
#         sqlite3_connect: Connection,
#     ):
#         """Проверка записей genre_film_work."""
#         sqlite3_cursor = sqlite3_connect.cursor()
#         pg_cursor = pg_connect.cursor()

#         sqlite3_query = """
#             SELECT "created_at", "id", "film_work_id", "genre_id"
#             FROM genre_film_work
#         """
#         sqlite3_rows = sqlite3_cursor.execute(sqlite3_query)

#         pg_query = """
#             SELECT "created", "id", "film_work_id", "genre_id"
#             FROM "content"."genre_film_work" WHERE id = '{0}'
#         """

#         for row in sqlite3_rows.fetchall():
#             sqlite3_data = GenreFilmWork(*row)
#             pg_cursor.execute(pg_query.format(sqlite3_data.id))
#             pg_data = GenreFilmWork(*pg_cursor.fetchone())
#             assert sqlite3_data == pg_data

#     def test_person_records(
#         self,
#         pg_connect: connection,
#         sqlite3_connect: Connection,
#     ):
#         """Проверка записей person."""
#         sqlite3_cursor = sqlite3_connect.cursor()
#         pg_cursor = pg_connect.cursor()

#         sqlite3_query = """
#             SELECT "created_at", "updated_at", "id", "full_name"
#             FROM person
#         """
#         sqlite3_rows = sqlite3_cursor.execute(sqlite3_query)

#         pg_query = """
#             SELECT "created", "modified", "id", "full_name"
#             FROM "content"."person" WHERE id = '{0}'
#         """

#         for row in sqlite3_rows.fetchall():
#             sqlite3_data = Person(*row)
#             pg_cursor.execute(pg_query.format(sqlite3_data.id))
#             pg_data = Person(*pg_cursor.fetchone())
#             assert sqlite3_data == pg_data

#     def test_person_film_work_records(
#         self,
#         pg_connect: connection,
#         sqlite3_connect: Connection,
#     ):
#         """Проверка записей person_film_work."""
#         sqlite3_cursor = sqlite3_connect.cursor()
#         pg_cursor = pg_connect.cursor()

#         sqlite3_query = """
#             SELECT "created_at", "id", "film_work_id", "person_id", "role"
#             FROM person_film_work
#         """
#         sqlite3_rows = sqlite3_cursor.execute(sqlite3_query)

#         pg_query = """
#             SELECT "created", "id", "film_work_id", "person_id", "role"
#             FROM "content"."person_film_work" WHERE id = '{0}'
#         """

#         for row in sqlite3_rows.fetchall():
#             sqlite3_data = PersonFilmWork(*row)
#             pg_cursor.execute(pg_query.format(sqlite3_data.id))
#             pg_data = PersonFilmWork(*pg_cursor.fetchone())
#             assert sqlite3_data == pg_data
