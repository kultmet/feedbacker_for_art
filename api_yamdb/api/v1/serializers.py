from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    Review, Comment, Title
)


class ReviewSerializer(serializers.ModelSerializer):
    # author = SlugRelatedField(slug_field='username', read_only=True)
    #
    # class Meta:
    #     fields = '__all__'
    #     model = Post
    pass


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)
