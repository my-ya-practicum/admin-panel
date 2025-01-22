#!/bin/sh

# 0. Ждем пока ответит БД
echo "Waiting for db.."
poetry run python3 app/manage.py check --database default
until [ $? -eq 0 ];
do
    echo "Waiting for postgres..."
    sleep 0.2
    poetry run python3 app/manage.py check --database default
done
echo "PostgreSQL started"

# 1. Применение миграций
poetry run python3 app/manage.py migrate --noinput

# 2. Сбор статики
# poetry run python3 app/manage.py collectstatic --no-input

# 3. Компиляция переводов
poetry run python3 app/manage.py compilemessages -l en -l ru

# 4. Создание суперпользователя
poetry run python3 app/manage.py createsuperuser --noinput || true

poetry run python3 app/manage.py runserver 0.0.0.0:8000

# # 5. Запуск gunicorn или dev сервера
# if [ $DEBUG = 1 ]; then
#     python3 app/manage.py runserver 0.0.0.0:8000
# else
#     gunicorn --config=config/gunicorn.py config.wsgi
# fi