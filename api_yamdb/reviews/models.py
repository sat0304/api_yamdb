import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg

from users.models import User

CHOICES_CATEGORY = (
    ('Books', 'Книги'),
    ('Films', 'Фильмы'),
    ('Music', 'Музыка'),
)

CHOICES_GENRE = (
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


def movie_year_validator(value):
    """Функция проверки года выпуска фильма."""
    if value < 1896 or value > datetime.datetime.now().year:
        raise ValidationError(f'%{value}s неправильный год!')


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(
        'Наименование категории',
        max_length=256)
    slug = models.SlugField(
        'Уникальный адрес категории',
        max_length=50,
        unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'Категории'

    def __str__(self) -> str:
        return self.slug


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(
        'Наименование жанра',
        max_length=256)
    slug = models.SlugField(
        'Уникальный адрес жанра',
        max_length=50,
        unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'Жанры'

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Произведение."""
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='category',
        blank=True,
        null=False,
        verbose_name='Категория')
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='GenreTitle')
    name = models.CharField(
        'Название произведения',
        max_length=256,
        blank=False)
    year = models.PositiveIntegerField(
        'Год выпуска',
        db_index=True,
        validators=(movie_year_validator,))
    rating = models.IntegerField(
        'Рейтинг поста',
        null=True,
        help_text='Введите текст поста',)
    description = models.TextField(
        'Описание произведения',
        blank=True,
        help_text='Введите текст поста')

    class Meta:
        ordering = ('-year', )
        verbose_name = 'Произведения'

    def __str__(self) -> str:
        return f'Произведение {self.name}, рейтинг {self.rating}'


class GenreTitle(models.Model):
    """Связанная таблица жанров и произведений."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT,
        related_name='genre',
        blank=True,
        null=False,
        verbose_name='Жанр')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE)

    class Meta:
        ordering = ('genre', )
        verbose_name = 'Жанры_произведений'

    def __str__(self) -> str:
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Таблица отзывов на произведение."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveIntegerField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date', )
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title_id',),
                name='unique_review'
            )
        ]

    def __str__(self) -> str:
        return self.text

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.score_avg = Review.objects.filter(title_id=self.title).aggregate(
            Avg('score')
        )
        self.title.rating = self.score_avg['score__avg']
        self.title.save()


class Comment(models.Model):
    """Таблица комментариев на отзывы к произведениям."""
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(null=True, blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Комментарии_произведений'

    def __str__(self) -> str:
        return self.text
