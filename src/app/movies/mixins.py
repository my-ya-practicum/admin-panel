from uuid import uuid4
from django.db import models


class TimeStampedMixin(models.Model):
    """Миксин для timestamps."""

    # auto_now_add=True - выставить дату добавления
    created = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    # auto_now=True - выставить дату при каждом обновлении
    modified = models.DateTimeField(
        auto_now=True,
        null=True,
    )

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """Миксин для id = uuid."""

    # editable=False - не показывать id для редактирования в админке
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True
