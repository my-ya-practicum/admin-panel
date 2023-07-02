from django.db import models
from django.utils.translation import gettext_lazy as _


class FilmTypeEnum(models.TextChoices):
    """Справочник типов фильмов."""

    movie = "movie", _("Movie")
    tv_show = "tv_show", _("TV Show")


class PersonRoleEnum(models.TextChoices):
    """Справочник ролей участников фильма."""

    producer = "producer", _("Producer")
    actor = "actor", _("Actor")
    writer = "writer", _("Writer")
    director = "director", _("Director")
