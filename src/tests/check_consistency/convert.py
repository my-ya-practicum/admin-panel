from datetime import datetime
from uuid import UUID

from script.sqlite_to_postgres.etl_movies.dto.film_work import (
    FilmWorkDTO,
    GenreDTO,
    GenreFilmWorkDTO,
    PersonDTO,
    PersonFilmWorkDTO,
)


class Converter:
    @staticmethod
    def convert_sqlite_row_to_dto(row: dict) -> FilmWorkDTO:
        return FilmWorkDTO(
            id=UUID(row["id"]),
            title=row["title"],
            description=row["description"],
            creation_date=row["creation_date"],
            rating=row["rating"],
            type=row["type"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    @staticmethod
    def convert_sqlite_row_to_genre_dto(row: dict) -> GenreDTO:
        """Преобразует строку из SQLite в объект GenreDTO."""
        return GenreDTO(
            id=UUID(row["id"]),
            name=row["name"],
            description=row["description"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    @staticmethod
    def convert_sqlite_row_to_genre_film_work_dto(row: dict) -> GenreFilmWorkDTO:
        """Преобразует строку из SQLite в объект GenreFilmWorkDTO."""
        return GenreFilmWorkDTO(
            id=UUID(row["id"]),
            film_work_id=UUID(row["film_work_id"]),
            genre_id=UUID(row["genre_id"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    @staticmethod
    def convert_sqlite_row_to_person_dto(row: dict) -> PersonDTO:
        """Преобразует строку из SQLite в объект PersonDTO."""
        return PersonDTO(
            id=UUID(row["id"]),
            full_name=row["full_name"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    @staticmethod
    def convert_sqlite_row_to_person_film_work_dto(row: dict) -> PersonFilmWorkDTO:
        """Преобразует строку из SQLite в объект PersonFilmWorkDTO."""
        return PersonFilmWorkDTO(
            id=UUID(row["id"]),
            film_work_id=UUID(row["film_work_id"]),
            person_id=UUID(row["person_id"]),
            role=row["role"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )
