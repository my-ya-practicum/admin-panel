from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class FilmWorkDTO:
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
    created_at: datetime
