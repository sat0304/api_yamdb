from django.db import models
from django.db.models import Avg

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
        ordering = ('name', )
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
        ordering = ('name', )
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
                                null=True,
                                help_text='Введите текст поста',
                                )
    description = models.TextField('Описание произведения',
                                   blank=True,
                                   null=True,
                                   help_text='Введите текст поста')

    def __str__(self):
        return f'Произведение {self.name}, рейтинг {self.rating}'

    class Meta:
        ordering = ('-year', )
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

    class Meta:
        ordering = ('genre', )
        verbose_name = "Жанры_произведений"


class Review(models.Model):
    """Таблица, содержащая отзывы на произведение."""
    SCORES = zip(range(1, 11), range(1, 11))
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.IntegerField(choices=SCORES, default=1)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Жанр'

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
    """Таблица, содержащая комментарии к отзывам на произведение."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации комментария',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text
