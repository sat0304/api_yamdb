from rest_framework import serializers

from .models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def validate_score(self, value):
        if value not in range(1, 11):
            raise serializers.ValidationError('Выбери оценку от 1 до 10')
        return value

    def validate(self, data):
        if (
            Review.objects.filter(
                author=self.context.get('request').user,
                title_id=self.context.get('view').kwargs.get('title_id')
            ).exists()
            and self.context.get('request').method == 'POST'
        ):
            raise serializers.ValidationError(
                'Возможен только один отзыв на произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    review_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {'text': {'required': True}}
