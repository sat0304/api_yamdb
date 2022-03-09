from django.contrib import admin
from api_yamdb import settings

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    empty_value_display = settings.CELL_NULL
