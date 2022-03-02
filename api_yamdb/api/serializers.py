from rest_framework import serializers

from reviews.models import Category, Genre, Titles


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Titles
        fields = ('__all__')
