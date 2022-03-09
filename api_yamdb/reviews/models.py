from django.db import models
from django.db.models import Avg

from users.models import User


class Category(models.Model):
    """Таблица, содержащая категории произведений."""
    name = models.CharField(max_length=254)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Таблица, содержащая жанр произведения."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Таблица, содержащая название произведения."""
    name = models.CharField(
        max_length=150,
        verbose_name='Название'
    )
    year = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name='Год'
    )
    description = models.TextField(
        max_length=200,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genre'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='categories'
    )
    rating = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Рейтинг'
    )

    class Meta:
        verbose_name = 'Произведение'

    def __str__(self) -> str:
        return self.name


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
