from django.contrib import admin

from api_yamdb import settings

from reviews.models import Category, Genre, Title


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    list_editable = ('name',)
    search_fields = ('slug',)
    list_filter = ('slug',)
    empty_value_display = settings.CELL_NULL


@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    list_editable = ('name',)
    search_fields = ('slug',)
    list_filter = ('slug',)
    empty_value_display = settings.CELL_NULL


admin.site.register(Title)
