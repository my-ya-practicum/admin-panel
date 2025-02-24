import pytest
import sqlite3
import psycopg

from script.sqlite_to_postgres.etl_movies.settings import Settings

settings = Settings()


@pytest.fixture
def sqlite3_connect():
    try:
        connect = sqlite3.connect(settings.sqlite_config.sqlite_db_file_path)
        yield connect
    finally:
        connect.close()


@pytest.fixture
def pg_connect():
    try:
        connect = psycopg.connect(settings.postgres_config.database_url)
        yield connect
    finally:
        connect.close()
