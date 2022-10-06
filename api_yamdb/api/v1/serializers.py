from rest_framework import serializers

from reviews.models import Category, Genre, Title


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с жанрами"""
    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для работы с категориями"""
    class Meta:
        model = Category
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с произведениями"""
    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=False, read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
