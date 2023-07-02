FROM python:3.10

# Основной путь приложения
ENV SRC_DIR=/opt

# Путь до приложения django
ENV APP_DIR=$SRC_DIR/app

ENV APP_USER=backend-user

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    GUNICORN_PROCESSES 4 \
    GUNICORN_CONNECTIONS 8 \
    GUNICORN_LOGLEVEL 'error' \
    DJANGO_SETTINGS_MODULE 'config.settings'

# Утановка доп. утилит
RUN apt-get update && \
    apt-get install -y gettext && \
    rm -rf /var/lib/apt/lists/*

# Создание no-root пользователя
RUN groupadd -r $APP_USER && \
    useradd -d $SRC_DIR -r -g $APP_USER $APP_USER && \
    chown $APP_USER:$APP_USER -R $SRC_DIR

USER $APP_USER

# Установка зависимостей
WORKDIR $SRC_DIR

ENV PATH="/$SRC_DIR/.local/bin:${PATH}"
RUN pip install --user --upgrade pip && \
    pip install --user --no-cache-dir poetry

COPY pyproject.toml pyproject.toml
RUN poetry install --no-root

WORKDIR $APP_DIR

# Копирования кода приложения
COPY ./src/app $APP_DIR

EXPOSE 8000

COPY docker/django/entrypoint.sh /usr/local/bin/entrypoint.sh
