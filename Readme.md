# Intro

* link = https://github.com/my-ya-practicum/movies-admin-panel

# Init development

1) init poetry
```bash
poetry install --no-root
```

2) env
```
cp ./.docker.env.template ./.docker.env
cp ./src/.env.template ./src/.env
```

`POSTGRES_USER=DB_USER=` - пользователь БД
`POSTGRES_PASSWORD=DB_PASSWORD=` - пароль пользователя

3) up docker local
```bash
make up-local
```

4) go = http://localhost/admin/

5) load data from sqlite
```bash
cp ./.env.local.template ./.env.local
```

`DB_USER=` - пользователь БД
`DB_PASSWORD=` - пароль пользователя

```bash
withenv ./.env.local poetry run python3 ./sqlite_to_postgres/load_data.py
```

6) test data
```bash
withenv ./.env.local poetry run pytest ./sqlite_to_postgres/
```


# TODO:
+ запуск gunicorn + config
+ static data из django

