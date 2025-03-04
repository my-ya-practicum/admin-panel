"""
withenv .env poetry run pytest -vv ./src/tests/check_consistency/
"""

import sqlite3
import psycopg
from psycopg.rows import dict_row

from dataclasses import fields

from script.sqlite_to_postgres.etl_movies.dto.film_work import (
    FilmWorkDTO,
    GenreDTO,
    GenreFilmWorkDTO,
    PersonDTO,
    PersonFilmWorkDTO,
)
from tests.check_consistency.convert import Converter


def test_film_work_records(
    pg_connect: psycopg.Connection,
    sqlite3_connect: sqlite3.Connection,
):
    """Проверка записей film_work."""
    sqlite3_cursor = sqlite3_connect.cursor()
    pg_cursor = pg_connect.cursor(row_factory=dict_row)

    field_names = [field.name for field in fields(FilmWorkDTO)]

    sqlite3_query = f"SELECT {', '.join(field_names)} FROM film_work"
    sqlite3_cursor.execute(sqlite3_query)
    sqlite3_rows = sqlite3_cursor.fetchall()

    pg_query = f"SELECT {', '.join(field_names)} FROM content.film_work WHERE id = %s"

    for sqlite3_row in sqlite3_rows:
        sqlite3_data = FilmWorkDTO(**dict(sqlite3_row))
        sqlite3_data = Converter.convert_sqlite_row_to_dto(dict(sqlite3_row))
        pg_cursor.execute(pg_query, (sqlite3_data.id,))  # type: ignore
        pg_row = pg_cursor.fetchone()
        if pg_row:
            pg_data = FilmWorkDTO(**pg_row)
            assert sqlite3_data == pg_data
        else:
            raise AssertionError(f"Record with id {sqlite3_data.id} not found in PostgreSQL")


def test_genre_records(
    pg_connect: psycopg.Connection,
    sqlite3_connect: sqlite3.Connection,
):
    """Проверка записей genre."""
    sqlite3_cursor = sqlite3_connect.cursor()
    pg_cursor = pg_connect.cursor(row_factory=dict_row)

    field_names = [field.name for field in fields(GenreDTO)]

    sqlite3_query = f"SELECT {', '.join(field_names)} FROM genre"
    sqlite3_cursor.execute(sqlite3_query)
    sqlite3_rows = sqlite3_cursor.fetchall()

    pg_query = f"SELECT {', '.join(field_names)} FROM content.genre WHERE id = %s"

    for sqlite3_row in sqlite3_rows:
        sqlite3_data = Converter.convert_sqlite_row_to_genre_dto(dict(sqlite3_row))
        pg_cursor.execute(pg_query, (sqlite3_data.id,))  # type: ignore
        pg_row = pg_cursor.fetchone()

        if pg_row:
            pg_data = GenreDTO(**pg_row)
            assert sqlite3_data == pg_data
        else:
            raise AssertionError(f"Record with id {sqlite3_data.id} not found in PostgreSQL")


def test_genre_film_work_records(
    pg_connect: psycopg.Connection,
    sqlite3_connect: sqlite3.Connection,
):
    """Проверка записей genre_film_work."""
    sqlite3_cursor = sqlite3_connect.cursor()
    pg_cursor = pg_connect.cursor(row_factory=dict_row)
    field_names = [field.name for field in fields(GenreFilmWorkDTO)]

    sqlite3_query = f"SELECT {', '.join(field_names)} FROM genre_film_work"
    sqlite3_cursor.execute(sqlite3_query)
    sqlite3_rows = sqlite3_cursor.fetchall()

    pg_query = f"SELECT {', '.join(field_names)} FROM content.genre_film_work WHERE id = %s"

    for sqlite3_row in sqlite3_rows:
        sqlite3_data = Converter.convert_sqlite_row_to_genre_film_work_dto(dict(sqlite3_row))

        pg_cursor.execute(pg_query, (sqlite3_data.id,))  # type: ignore
        pg_row = pg_cursor.fetchone()

        if pg_row:
            pg_data = GenreFilmWorkDTO(**pg_row)
            assert sqlite3_data == pg_data
        else:
            raise AssertionError(f"Record with id {sqlite3_data.id} not found in PostgreSQL")


def test_person_records(
    pg_connect: psycopg.Connection,
    sqlite3_connect: sqlite3.Connection,
):
    """Проверка записей person."""
    sqlite3_cursor = sqlite3_connect.cursor()
    pg_cursor = pg_connect.cursor(row_factory=dict_row)

    field_names = [field.name for field in fields(PersonDTO)]

    sqlite3_query = f"SELECT {', '.join(field_names)} FROM person"
    sqlite3_cursor.execute(sqlite3_query)
    sqlite3_rows = sqlite3_cursor.fetchall()

    pg_query = f"SELECT {', '.join(field_names)} FROM content.person WHERE id = %s"

    for sqlite3_row in sqlite3_rows:
        sqlite3_data = Converter.convert_sqlite_row_to_person_dto(dict(sqlite3_row))

        pg_cursor.execute(pg_query, (sqlite3_data.id,))  # type: ignore
        pg_row = pg_cursor.fetchone()

        if pg_row:
            pg_data = PersonDTO(**pg_row)
            assert sqlite3_data == pg_data
        else:
            raise AssertionError(f"Record with id {sqlite3_data.id} not found in PostgreSQL")


def test_person_film_work_records(
    pg_connect: psycopg.Connection,
    sqlite3_connect: sqlite3.Connection,
):
    """Проверка записей person_film_work."""
    sqlite3_cursor = sqlite3_connect.cursor()
    pg_cursor = pg_connect.cursor(row_factory=dict_row)
    field_names = [field.name for field in fields(PersonFilmWorkDTO)]

    sqlite3_query = f"SELECT {', '.join(field_names)} FROM person_film_work"
    sqlite3_cursor.execute(sqlite3_query)
    sqlite3_rows = sqlite3_cursor.fetchall()

    pg_query = f"SELECT {', '.join(field_names)} FROM content.person_film_work WHERE id = %s"

    for sqlite3_row in sqlite3_rows:
        sqlite3_data = Converter.convert_sqlite_row_to_person_film_work_dto(dict(sqlite3_row))

        pg_cursor.execute(pg_query, (sqlite3_data.id,))  # type: ignore
        pg_row = pg_cursor.fetchone()

        if pg_row:
            pg_data = PersonFilmWorkDTO(**pg_row)
            assert sqlite3_data == pg_data
        else:
            raise AssertionError(f"Record with id {sqlite3_data.id} not found in PostgreSQL")
