from django.contrib import admin
from api_yamdb import settings

from .models import User

admin.site.register(User)
