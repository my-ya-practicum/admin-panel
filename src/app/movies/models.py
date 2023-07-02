from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from movies.mixins import TimeStampedMixin, UUIDMixin
from movies.enums import FilmTypeEnum, PersonRoleEnum


class FilmWork(UUIDMixin, TimeStampedMixin):
    """Модель кинопроизведений."""

    title = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name=_("Title"),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
    )
    creation_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Creation Date"),
    )
    type = models.CharField(
        max_length=127,
        choices=FilmTypeEnum.choices,
        verbose_name=_("Type"),
    )
    rating = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name=_("Rating"),
    )
    file_path = models.FileField(
        blank=True,
        null=True,
        verbose_name=_("File path"),
    )

    def __str__(self):
        """Для строкового представления используем название фильма."""
        return self.title

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("Film Work")
        verbose_name_plural = _("Film Works")
        indexes = [
            models.Index(
                fields=["creation_date"],
                name="film_work_creation_date_idx",
            ),
        ]

    genres = models.ManyToManyField("Genre", through="GenreFilmWork")
    persons = models.ManyToManyField("Person", through="PersonFilmWork")


class Genre(UUIDMixin, TimeStampedMixin):
    """Модель жанров."""

    name = models.CharField(
        max_length=255,
        null=False,
        verbose_name=_("Name"),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
    )

    def __str__(self):
        """Для строкового представления используем название жанра."""
        return self.name

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")


class GenreFilmWork(UUIDMixin):
    """Связь жанров с фильмами."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name=_("Genre"),
    )
    film_work = models.ForeignKey(
        "FilmWork",
        on_delete=models.CASCADE,
        verbose_name=_("Film work"),
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")
        db_table = 'content"."genre_film_work'
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "genre"],
                name="genre_film_work_idx",
            ),
        ]


class Person(UUIDMixin, TimeStampedMixin):
    """Модель участников фильма."""

    full_name = models.CharField(
        max_length=255,
        verbose_name=_("Full Name"),
    )

    def __str__(self):
        """Для строкового представления используем ФИО участника."""
        return self.full_name

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")


class PersonFilmWork(UUIDMixin):
    """Модель-связка участника с фильмом и его ролью."""

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name=_("Person"),
    )
    film_work = models.ForeignKey(
        FilmWork,
        on_delete=models.CASCADE,
        verbose_name=_("Film work"),
    )

    role = models.CharField(
        max_length=127,
        null=True,
        choices=PersonRoleEnum.choices,
        verbose_name=_("Role"),
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
        db_table = 'content"."person_film_work'
        constraints = [
            models.UniqueConstraint(
                fields=["person", "film_work", "role"],
                name="person_film_work_role_idx",
            ),
        ]
