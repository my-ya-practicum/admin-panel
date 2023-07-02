from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from movies.models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Управление жанрами."""

    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Управление участниками кинопроизведения."""

    list_display = ('full_name',)
    search_fields = ('full_name',)


class GenreFilmWorkInline(admin.TabularInline):
    """Вложенная форма жанра кинопроизведения."""

    model = GenreFilmWork
    autocomplete_fields = ['genre']


class PersonFilmWorkInline(admin.TabularInline):
    """Вложенная форма участника кинопроизведения."""

    model = PersonFilmWork
    autocomplete_fields = ['person']


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    """Управление кинопроизведениями."""

    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)
    list_display = ('title', 'type', 'get_genres', 'creation_date', 'rating')
    list_prefetch_related = ('genres')
    list_filter = ('type',)
    search_fields = ('id', 'title', 'description')

    def get_queryset(self, request):
        """Предзагрузка жанров."""
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(self.list_prefetch_related)
        )
        return queryset

    @admin.display(description=_('Film Genres'))
    def get_genres(self, obj):
        """Перечисление жанров на списке кинопроизведений."""
        return ', '.join([genre.name for genre in obj.genres.all()])
