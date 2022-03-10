from django.db import models
from django.contrib.auth import get_user_model
from users.models import User

CHOICES_CATEGORY = (
    ('Books', 'Книги'),
    ('Films', 'Фильмы'),
    ('Music', 'Музыка'),
)

CHOICES_GENRE= (
    ('Fairytale', 'Сказка'),
    ('Rock', 'Рок'),
    ('ArtHouse', 'Артхаус'),
    ('Comedy', 'Комедия'),
    ('Thriller', 'Триллер'),
    ('Fantasy', 'Фантастика'),
    ('Classic', 'Классика'),
    ('Detective', 'Детектив'),
    ('Horrors', 'Ужасы'),
    ('Pop', 'Поп'),
    ('Chanson', 'Шансон'),
)

class Category(models.Model):
    """Категории произведений."""
    name = models.CharField('Наименование категории',
                            #choices=CHOICES_CATEGORY,
                            max_length=256)
    slug = models.SlugField('Уникальный адрес категории',
                            max_length=50,
                            unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = "Категории"


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField('Наименование жанра',
                            #choices=CHOICES_GENRE,
                            max_length=256)
    slug = models.SlugField('Уникальный адрес жанра',
                            max_length=50,
                            unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанры"

class Title(models.Model):
    """Произведение."""
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 related_name="category",
                                 blank=True,
                                 null=False,
                                 verbose_name='Категория')
    genre = models.ManyToManyField(Genre,
                                   verbose_name='Жанр',
                                   through='GenreTitle')    
    """genre = models.ForeignKey(Genre, #ForeignKey
                              on_delete=models.PROTECT,
                              related_name="genre",
                              blank=True,
                              null=False,
                              verbose_name='Жанр')"""
    name = models.CharField('Название произведения',
                            max_length=256,
                            blank=False)
    year = models.PositiveIntegerField('Год выпуска',
                                       db_index=True,)
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

class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre,
                              on_delete=models.PROTECT,
                              related_name="genre",
                              blank=True,
                              null=False,
                              verbose_name='Жанр')
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
