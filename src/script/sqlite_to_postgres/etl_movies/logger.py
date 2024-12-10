from script.sqlite_to_postgres.etl_movies.settings import Settings


LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DEFAULT_HANDLERS = ["console"]


settings = Settings()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": LOG_FORMAT,
        },
    },
    "handlers": {
        "console": {
            "level": settings.logger_config.log_level,
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        # "default": {
        #     "formatter": "default",
        #     "class": "logging.StreamHandler",
        #     "stream": "ext://sys.stdout",
        # },
    },
    "loggers": {
        "": {
            "handlers": LOG_DEFAULT_HANDLERS,
            "level": settings.logger_config.log_level,
        },
    },
    "root": {
        "level": settings.logger_config.log_level,
        "formatter": "verbose",
        "handlers": LOG_DEFAULT_HANDLERS,
    },
}
