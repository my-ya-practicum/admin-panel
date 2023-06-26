from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


@dataclass
class UUIDMixin:
    """Миксин для id uuid."""

    id: UUID = field(default_factory=uuid4)


class Base(object):
    """Абстрактный класс для created и modified."""

    def __post_init__(self):
        """Abstract post_init."""
        pass


@dataclass
class CreatedMixin(Base):
    """Миксин для даты создания записи."""

    created: Optional[datetime] = field(metadata={'alias': 'created_at'})

    def __post_init__(self):
        """Преобразование из строки в datetime объект."""
        super().__post_init__()
        if self.created:
            if isinstance(self.created, str):
                self.created = datetime.fromisoformat(self.created.split('.')[0])
            self.created = self.created.strftime(DATETIME_FORMAT)


@dataclass
class ModifiedMixin(Base):
    """Миксин для даты модификации записи."""

    modified: Optional[datetime] = field(metadata={'alias': 'updated_at'})

    def __post_init__(self):
        """Преобразование из строки в datetime объект."""
        super().__post_init__()
        if self.modified:
            if isinstance(self.modified, str):
                self.modified = datetime.fromisoformat(self.modified.split('.')[0])
            self.modified = self.modified.strftime(DATETIME_FORMAT)


@dataclass
class BaseModel:
    """Базовый класс для моделей."""

    @classmethod
    def from_sqlite(cls, **kwargs):
        """Преобразование данных из sqlite."""
        for dataclass_field in cls.__dataclass_fields__.values():
            if alias := dataclass_field.metadata.get('alias'):
                if alias in kwargs:
                    kwargs[dataclass_field.name] = kwargs[alias]
                    del kwargs[alias]
        return cls(**kwargs)


@dataclass
class FilmWork(BaseModel, UUIDMixin, CreatedMixin, ModifiedMixin):
    """Модель кинопроизведений."""

    title: str = ''
    type: str = ''
    description: Optional[str] = None
    creation_date: Optional[date] = None
    rating: Optional[float] = None
    file_path: Optional[str] = None


@dataclass
class Genre(BaseModel, UUIDMixin, CreatedMixin, ModifiedMixin):
    """Модель жанров."""

    name: str = ''
    description: Optional[str] = None


@dataclass
class GenreFilmWork(BaseModel, UUIDMixin, CreatedMixin):
    """Модель для связи кинопроизведений и жанров."""

    film_work_id: Optional[UUID] = None
    genre_id: Optional[UUID] = None


@dataclass
class Person(BaseModel, UUIDMixin, CreatedMixin, ModifiedMixin):
    """Модель участников."""

    full_name: str = ''


@dataclass
class PersonFilmWork(BaseModel, UUIDMixin, CreatedMixin):
    """Модель для связи кинопроизведений и участников."""

    film_work_id: Optional[UUID] = None
    person_id: Optional[UUID] = None
    role: Optional[str] = None
