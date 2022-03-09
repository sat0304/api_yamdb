from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

ROLE_CHOICES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    username = models.CharField('Логин',
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
    email = models.EmailField('e-mail',
                              max_length=254,
                              unique=True,
                              help_text='Электронная почта',
                              )
    first_name = models.CharField('Имя',
                                  max_length=150,
                                  blank=True,
                                  null=True,
                                  help_text='Имя пользователя',
                                  )
    last_name = models.CharField('Имя',
                                 max_length=150,
                                 blank=True,
                                 null=True,
                                 help_text='Фамилия пользователя',
                                 )
    bio = models.TextField('Биография',
                           blank=True,
                           null=True,
                           help_text='Биография пользователя',
                           )
    role = models.TextField('Роль',
                            choices=ROLE_CHOICES,
                            default='user',
                            help_text='Роль пользователя',
                            )

    def __str__(self) -> str:
        return self.username
