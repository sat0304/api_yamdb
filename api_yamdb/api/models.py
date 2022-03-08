from django.db import models


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
