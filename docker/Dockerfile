FROM python:3.12-slim

# Утановка доп. утилит
RUN apt-get update && \
    apt-get install -y gettext && \
    rm -rf /var/lib/apt/lists/*

# Основной путь приложения
ENV SRC_DIR=/opt

# Путь до приложения django
ENV APP_DIR=$SRC_DIR/app

ENV PYTHONPATH=$SRC_DIR \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1

# Установка зависимостей
WORKDIR $SRC_DIR

RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry install --no-root --only main

# Копирования кода приложения
COPY src/app $APP_DIR
COPY docker/django/entrypoint.sh /usr/local/bin/entrypoint.sh

EXPOSE 8000
