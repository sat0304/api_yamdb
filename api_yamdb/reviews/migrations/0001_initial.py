# Generated by Django 2.2.16 on 2022-03-10 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Наименование категории')),
                ('slug', models.SlugField(unique=True, verbose_name='Уникальный адрес категории')),
            ],
            options={
                'verbose_name': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации комментария')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Наименование жанра')),
                ('slug', models.SlugField(unique=True, verbose_name='Уникальный адрес жанра')),
            ],
            options={
                'verbose_name': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('score', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=1)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации отзыва')),
            ],
            options={
                'verbose_name': 'Жанр',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название произведения')),
                ('year', models.PositiveIntegerField(db_index=True, verbose_name='Год выпуска')),
                ('rating', models.IntegerField(help_text='Введите текст поста', verbose_name='Рейтинг поста')),
                ('description', models.TextField(blank=True, help_text='Введите текст поста', null=True, verbose_name='Описание произведения')),
                ('category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='category', to='reviews.Category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(through='reviews.GenreTitle', to='reviews.Genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Произведения',
            },
        ),
    ]
