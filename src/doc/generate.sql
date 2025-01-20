-- Устанавливаем расширения для генерации UUID
CREATE EXTENSION "uuid-ossp";

-- Генерируем данные в интервале с 1900 по 2021 год с шагом в час. В итоге сгенерируется 1060681 записей

INSERT INTO content.film_work (id, title, type, creation_date, rating)
SELECT uuid_generate_v4(),
    'some name',
    case
        when RANDOM() < 0.3 THEN 'movie'
        ELSE 'tv_show'
    END,
    date::DATE,
    floor(random() * 100)
FROM generate_series(
        '1900-01-01'::DATE,
        '3024-01-01'::DATE,
        '1 hour'::interval
    ) date;

explain analyze
SELECT id
FROM content.film_work
where creation_date = '2024-01-01';