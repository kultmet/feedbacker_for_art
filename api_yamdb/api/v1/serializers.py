from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    Review, Comment, Title
)


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
                  'author',
                  'score',
                  'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field='text', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id',
                  'text',
                  'author',
                  'pub_date')
