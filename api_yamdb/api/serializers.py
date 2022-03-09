from rest_framework import serializers

from reviews.models import Category, Genre, Title, GenreTitles


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
    genre = GenreSerializer(many=True)
    category = serializers.SlugRelatedField(many=False, queryset=Category.objects.all(), slug_field='slug')
    #category = CategorySerializer(many=False)


    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            # То создаём запись о котике без его достижений
            titles = Title.objects.create(**validated_data)
            return titles
        
        # Уберем список достижений из словаря validated_data и сохраним его
        genres = validated_data.pop('genre')

        # Создадим нового котика пока без достижений, данных нам достаточно
        titles = Title.objects.create(**validated_data)

        # Для каждого достижения из списка достижений
        for genre in genres:
            # Создадим новую запись или получим существующий экземпляр из БД
            current_genre, status = Genre.objects.get_or_create(
                **genre)
            # Поместим ссылку на каждое достижение во вспомогательную таблицу
            # Не забыв указать к какому котику оно относится
            GenreTitles.objects.create(
                genre=current_genre, titles=titles)
        return titles


    
    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
