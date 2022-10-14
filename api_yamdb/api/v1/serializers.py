from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator


from reviews.models import Review, Comment, Title, Category, Genre
from users.models import User
from .utility import (
    generate_confirmation_code,
    send_email_with_verification_code
)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с жанрами произведений."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для работы с категориями."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializerRead(serializers.ModelSerializer):
    """Сериализатор для работы с произведениями при чтении."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'description', 'year', 'category', 'genre', 'rating'
        )
        read_only_fields = ('id',)

    def get_rating(self, obj):
        obj = obj.reviews.all().aggregate(rating=Avg('score'))
        return obj['rating']


class TitleSerializerCreate(serializers.ModelSerializer):
    """Сериализатор для работы с произведениями при создании."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'year', 'category', 'genre')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с отзывами."""
    author = SlugRelatedField(
        slug_field='username', read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'title', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if title.reviews.select_related('title').filter(author=author):
                raise ValidationError(
                    'Отзыв можно оставить один раз!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с отзывами."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field='text', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'review', 'author', 'pub_date')


class AdminUserSerializer(serializers.ModelSerializer):
    """Сериализатор для админа."""
    username = serializers.CharField(
        max_length=200,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username', },
        }
        validators = (
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            ),
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('А username не может быть "me"')
        return value


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""
    username = serializers.CharField(
        max_length=200,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    role = serializers.CharField(max_length=15, read_only=True)

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username', },
        }
        validators = (
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            ),
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('А username не может быть "me"')
        return value


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    """Сериализатор для получения кода подтверждения."""
    username = serializers.CharField(
        max_length=200,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = ('email', 'username')
        model = User
        validators = (
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            ),
        )

    def create(self, validated_data):
        validated_data['confirmation_code'] = generate_confirmation_code()
        user = User.objects.create_user(**validated_data)
        send_email_with_verification_code(validated_data)
        return user

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('А username не может быть "me"')
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField(
        max_length=250,
        write_only=True,
    )
    confirmation_code = serializers.CharField(
        max_length=255,
        write_only=True
    )

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        user_1 = User.objects.filter(
            username=user.username,
            confirmation_code=data['confirmation_code']
        ).exists()
        if not user_1:
            raise serializers.ValidationError(
                'Такого пользователя нет.'
            )
        return data
