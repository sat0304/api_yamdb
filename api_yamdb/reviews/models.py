from django.db import models
from django.contrib.auth import get_user_model
from users.models import User

CHOICES_CATEGORY = (
    ('Books', 'Книги'),
    ('Films', 'Фильмы'),
    ('Music', 'Музыка'),
    ('', 'ANY_one'),
    ('', 'ANY_two'),
)

CHOICES_GENRE= (
    ('Fairytale', 'Сказка'),
    ('Rock', 'Рок'),
    ('ArtHouse', 'Артхаус'),
    ('', 'ANY_one'),
    ('', 'ANY_two'),
)


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField('Наименование категории',
                            max_length=256)
    slug = models.SlugField('Уникальный адрес категории',
                            #choices=CHOICES_CATEGORY,
                            max_length=50,
                            unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = "Категории"


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField('Наименование жанра',
                            max_length=256)
    slug = models.SlugField('Уникальный адрес жанра',
                            #choices=CHOICES_GENRE,
                            max_length=50,
                            unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанры"

class Titles(models.Model):
    """Произведение."""
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 related_name="category",
                                 blank=True,
                                 null=False,
                                 verbose_name='Категория')
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitles')
    """genre = models.ForeignKey(Genre, #ForeignKey
                              on_delete=models.PROTECT,
                              related_name="genre",
                              blank=True,
                              null=False,
                              verbose_name='Жанр')"""
    name = models.CharField('Название произведения',
                            max_length=256)
    year = models.IntegerField('Год выпуска')
    rating = models.IntegerField('Рейтинг поста',
                              help_text='Введите текст поста')
    description = models.TextField('Описание произведения',
                                   blank=True,
                                   null=True,
                                   help_text='Введите текст поста')

    def __str__(self):
        return f'Произведение {self.name}, рейтинг {self.rating}'

    class Meta:
        verbose_name = "Произведения"

class GenreTitles(models.Model):
    genre = models.ForeignKey(Genre,
                              on_delete=models.PROTECT,
                              related_name="genre",
                              blank=True,
                              null=False,
                              verbose_name='Жанр')
    titles = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.titles}'
