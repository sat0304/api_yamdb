from rest_framework import serializers

from reviews.models import Category, Genre, Title, GenreTitle


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(many=False, queryset=Category.objects.all(), slug_field='slug')
    genre = GenreSerializer(many=True)

    """def get_rating(self, obj):
        reviews = Review.objects.filter(title_id=obj.pk)
        reviews_scores = reviews.values_list('score', flat=True)
        if reviews_scores:
            return int(sum(reviews_scores) / len(reviews_scores))
        return None"""


    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            titles = Title.objects.create(**validated_data)
            return titles

        genres = validated_data.pop('genre')
        titles = Titles.objects.create(**validated_data)
        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(**genre)
            GenreTitle.objects.create(genre=current_genre, titles=titles)
        return titles

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
