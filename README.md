# Локальный запуск

```bash
poetry env use $HOME/.pyenv/versions/3.12.6/bin/python3.12
poetry install --no-root
```

```
make up
```

```
cp .docker.env.example .docker.env
```

```
docker exec admin-movies poetry run python3 ./app/manage.py migrate
docker exec -it admin-movies poetry run python3 ./app/manage.py createsuperuser
```

```
cd /src/app
withenv ../../.env poetry run python3 manage.py makemigrations movies --settings=config.settings
```

```
cd /src/app
withenv ../../.env poetry run python3 manage.py makemessages -l en -l ru
withenv ../../.env poetry run python3 manage.py compilemessages -l en -l ru
```

# Проектное задание: панель администратора

Вам необходимо разработать сервис, который позволит создавать и редактировать записи в базе данных.

Критерии готовности:

- Интерфейс панели администратора настроен стандартными средствами Django.
- В нём можно создавать, редактировать и удалять кинопроизведения, жанры и персон.
- Связи между кинопроизведениями, жанрами и персонами заводятся на странице редактирования кинопроизведения.
- Вы используете базу данных, созданную на прошлом этапе.
- Системные таблицы Django не используют схему content.
- У вас описана initial-миграция, которая создаёт те же структуры, что и SQL из первого задания.
- Таблицы описаны в файле models.py.
- `settings.py` разбит на логические модули
- Поля created и modified проставляются автоматически.
- Чувствительные данные берутся из переменных окружения
- Все тексты переведены на русский с помощью `gettext_lazy`
