from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="postgres_")
    echo_log: bool = True
    load_chunk_size: int = 1000

    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    db: str = Field(default="movies_db")
    user: str = Field(default="movies_user")
    password: str = Field(default="movies_password")

    @property
    def database_url(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class SqliteConfig(BaseSettings):
    extract_chunk_size: int = 100
    sqlite_db_file_path: str = "db.sqlite"


class LoggerConfig(BaseSettings):
    log_level: str = 'DEBUG'


class Settings(BaseSettings):
    logger_config: LoggerConfig = LoggerConfig()
    sqlite_config: SqliteConfig = SqliteConfig()
    postgres_config: PostgresConfig = PostgresConfig()
