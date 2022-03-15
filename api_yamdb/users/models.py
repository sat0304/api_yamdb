from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from api_yamdb.settings import ROLE_CHOICES


class User(AbstractUser):
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
        help_text='Ник пользователя',
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+',
                message=('Ник должен быть '
                         + 'комбинацией букв,'
                         + 'цифр и символов @.+-_')
            )
        ]
    )
    password = models.CharField(
        'Пароль',
        max_length=128,
        blank=True,
        help_text='Пароль')
    email = models.EmailField(
        'e-mail',
        max_length=254,
        unique=True,
        help_text='Электронная почта',
    )
    confirmation_code = models.CharField(
        'Код',
        blank=True,
        max_length=9,
        help_text='Код подтверждения'
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
        help_text='Имя пользователя',
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
        help_text='Фамилия пользователя',
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        help_text='Биография пользователя',
    )
    role = models.TextField(
        'Роль',
        choices=ROLE_CHOICES,
        default='user',
        help_text='Роль пользователя',
    )

    class Meta:
        ordering = ('username',)

    def __str__(self) -> str:
        return self.username
