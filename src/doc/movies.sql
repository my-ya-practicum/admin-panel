
-- DROP SCHEMA content CASCADE;

CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp(0) NOT NULL DEFAULT now(),
    modified timestamp(0) NOT NULL DEFAULT now()
);

CREATE INDEX film_work_creation_date_idx ON content.film_work (creation_date);

CREATE TABLE IF NOT EXISTS content.genre (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp(0) NOT NULL DEFAULT now(),
    modified timestamp(0) NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS content.person (
    id UUID PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp(0) NOT NULL DEFAULT now(),
    modified timestamp(0) NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id UUID PRIMARY KEY,
    genre_id UUID NOT NULL,
    film_work_id UUID NOT NULL,
    created timestamp(0) NOT NULL DEFAULT now(),
    CONSTRAINT film_work_fkey
        FOREIGN KEY (film_work_id)
        REFERENCES content.film_work (id)
        ON DELETE CASCADE,
    CONSTRAINT genre_fkey
        FOREIGN KEY (genre_id)
        REFERENCES content.genre (id)
        ON DELETE CASCADE
);

CREATE UNIQUE INDEX genre_film_work_idx ON content.genre_film_work (film_work_id, genre_id);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id UUID PRIMARY KEY,
    person_id UUID NOT NULL,
    film_work_id UUID NOT NULL,
    role TEXT NOT NULL,
    created timestamp(0) NOT NULL DEFAULT now(),
    CONSTRAINT film_work_fkey
        FOREIGN KEY (film_work_id)
        REFERENCES content.film_work (id)
        ON DELETE CASCADE,
    CONSTRAINT person_fkey
        FOREIGN KEY (person_id)
        REFERENCES content.person (id)
        ON DELETE CASCADE
);

CREATE UNIQUE INDEX person_film_work_idx ON content.person_film_work (film_work_id, person_id, role);

