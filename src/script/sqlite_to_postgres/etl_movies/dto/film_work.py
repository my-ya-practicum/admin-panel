from dataclasses import dataclass
from uuid import UUID


@dataclass
class FilmWorkDTO:
    id: UUID
    title: str
    # description: str
