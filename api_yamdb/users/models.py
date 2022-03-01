from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    auth = models.TextField(
        'Аутентификация',
    )
