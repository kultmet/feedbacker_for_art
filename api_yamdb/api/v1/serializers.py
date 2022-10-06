from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    Review, Comment, Title
)


class TitleSerializer(serializers.ModelSerializer):     # временно

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )

    class Meta:
        model = Review
        fields = ('id',
                  'text',
                  'title',
                  'author',
                  'score',
                  'pub_date')
        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=('title', 'author'),
        #         message='Отзыв можно оставить один раз'
        #     )
        # ]

    def validate(self, data):
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(title=title_id, author=author).exists():
            raise ValidationError(
                'Отзыв можно оставить один раз!'
            )
        return data

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    # review = serializers.SlugRelatedField(
    #     slug_field='text', read_only=True
    # )

    class Meta:
        model = Comment
        fields = ('id',
                  'text',
                  # 'review',
                  'author',
                  'pub_date')
