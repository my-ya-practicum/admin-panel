import os
from functools import lru_cache

from dotenv import load_dotenv


class Config:
    """Конфигурационные данные для миграции."""

    SQLITE_PATH: str = os.getenv('SQLITE_PATH', 'sqlite_to_postgres/db.sqlite')
    DOTENV_PATH: str = 'postgres_to_es/.env'

    LOG_LEVEL: str = 'INFO'

    @property
    def postgres_dsn(self) -> dict:
        """Конфиг подключения к postgresql."""
        return {
            'dbname': os.getenv('DB_NAME', 'movies_database'),
            'user': os.getenv('DB_USER', 'app'),
            'password': os.getenv('DB_PASSWORD', '123qwe'),
            'host': os.getenv('DB_HOST', '127.0.0.1'),
            'port': os.getenv('DB_PORT', 5432),
        }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': LOG_LEVEL,
            },
        },
    }


@lru_cache
def get_config() -> Config:
    config = Config()
    load_dotenv(dotenv_path=config.DOTENV_PATH, verbose=True)
    return Config()
