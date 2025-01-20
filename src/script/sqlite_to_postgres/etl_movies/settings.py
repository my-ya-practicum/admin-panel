from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="postgres_")
    echo_log: bool = True

    host: str = Field(default="admin-database")
    port: int = Field(default=5432)
    db: str = Field(default="web_notepad")
    user: str = Field(default="movies_user")
    password: str = Field(default="movies_password")

    @property
    def database_url(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class SqliteConfig(BaseSettings):
    extract_chunk_size: int = 30
    sqlite_db_file_path: str = "db.sqlite"


class LoggerConfig(BaseSettings):
    log_level: str = 'DEBUG'


class Settings(BaseSettings):
    logger_config: LoggerConfig = LoggerConfig()
    sqlite_config: SqliteConfig = SqliteConfig()
    postgres_config: PostgresConfig = PostgresConfig()
