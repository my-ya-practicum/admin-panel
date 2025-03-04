from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from script.sqlite_to_postgres.etl_movies.dto.base import DTO


@dataclass
class FilmWorkDTO(DTO):
    id: UUID
    title: str
    description: str
    creation_date: datetime
    rating: datetime
    type: str
    created_at: datetime
    updated_at: datetime


@dataclass
class GenreDTO:
    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


@dataclass
class PersonDTO:
    id: UUID
    full_name: str
    created_at: datetime
    updated_at: datetime


@dataclass
class GenreFilmWorkDTO:
    id: UUID
    film_work_id: UUID
    genre_id: UUID
    created_at: datetime


@dataclass
class PersonFilmWorkDTO:
    id: UUID
    film_work_id: UUID
    person_id: UUID
    role: str
    created_at: datetime
