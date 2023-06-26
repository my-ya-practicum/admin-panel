import sqlite3

import psycopg2
from psycopg2.extras import DictCursor

import pytest

from sqlite_to_postgres.config import get_config

config = get_config()


@pytest.fixture()
def sqlite3_connect():
    try:
        connect = sqlite3.connect(config.SQLITE_PATH)
        yield connect
    finally:
        connect.close()


@pytest.fixture()
def pg_connect():
    try:
        connect = psycopg2.connect(**config.postgres_dsn, cursor_factory=DictCursor)
        yield connect
    finally:
        connect.close()
