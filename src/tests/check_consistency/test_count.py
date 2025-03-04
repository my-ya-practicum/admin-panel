import sqlite3
import psycopg


def test_count_film_works(
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
