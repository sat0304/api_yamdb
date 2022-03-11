from rest_framework import serializers

from .models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    """ Набор правил преобразования отзывов к произведениям."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('title', 'text', 'author', 'score', 'pub_date')
        model = Review
        
    def validate(self, data):
        super().validate(data)
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title_id = (
            self.context['request'].parser_context['kwargs']['title_id']
        )
        if Review.objects.filter(author=user, title__id=title_id).exists():
            raise serializers.ValidationError(
                "Можно оставить лишь один отзыв на данное произведение"
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """ Правила преобразования комментариев на отзывы к произведениям."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('review', 'text', 'author', 'pub_date',)
        model = Comment
