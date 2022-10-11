from django.contrib.auth import authenticate, models

from rest_framework.generics import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from django.db.models import Avg
from rest_framework.response import Response
from rest_framework import serializers, status

from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer, PasswordField, TokenObtainSlidingSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from reviews.models import (
    Review, Comment, Title, Category, Genre
)
from users.models import User


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        # exclude = ['id']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        # exclude = ['id']


class TitleSerializerRead(serializers.ModelSerializer):
    """Сериализатор для работы с произведениями при чтении"""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        # fields = '__all__'
        fields = ('id', 'name', 'description', 'year', 'category', 'genre', 'rating')
        read_only_fields = ('id',)
        # exclude = ('id',)

    def get_rating(self, obj):
        obj = obj.reviews.all().aggregate(rating=Avg('score'))
        return obj['rating']


class TitleSerializerCreate(serializers.ModelSerializer):
    """Сериализатор для работы с произведениями при создании"""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
        # many=False
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'
        # fields = ('name', 'description', 'year', 'category', 'genre')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с отзывами"""
    author = SlugRelatedField(
        slug_field='username', read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )
    # score = serializers.IntegerField()

    class Meta:
        model = Review
        fields = ('id',
                  'text',
                  'title',
                  'author',
                  'score',
                  'pub_date')

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    'Отзыв можно оставить один раз!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с отзывами"""
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
                  'review',
                  'author',
                  'pub_date')

# Дима



class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200)
    email = serializers.EmailField()


    class Meta:

        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username',},
        }
        validators = (
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            ), 
        )


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200, required=False)
    email = serializers.EmailField()

    class Meta:
        fields = ('email', 'username', 'confirmation_code')
        model = User
        permissions = (

        )
        # validators = (
        #     UniqueTogetherValidator(
        #         queryset=User.objects.all(),
        #         fields=['username', 'email']
        #     ),
            
        # )
    def validate_username(self, value):
            if value == 'me':
                raise serializers.ValidationError('А username не можеть быть "me"')
            return value



class MyObtainSerializer(TokenObtainSerializer):

    username_field = User().USERNAME_FIELD
    token_class = None

    default_error_messages = {
        "no_active_account": ("No active account found with the given credentials")
    }

    # class Meta:
    #     fields = ('username', 'confirmation_code')
        # extra_kwargs = {'password': {'required': False}}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["confirmation_code"] = serializers.IntegerField()
        # self.fields['password'] = serializers.CharField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "confirmation_code": attrs["confirmation_code"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass
        self.user = authenticate(**authenticate_kwargs)
        return {}


class MyTokenObtainPairSerializer(MyObtainSerializer):
    token_class = RefreshToken

    

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            models.update_last_login(None, self.user)

        return data

# class MyTokenObtainPairSerializer(serializers.ModelSerializer):
#     token_class = RefreshToken


#     def validate(self, attrs):
#         data = super().validate(attrs)

#         refresh = self.get_token(self.user)

#         data["refresh"] = str(refresh)
#         data["access"] = str(refresh.access_token)

#         if api_settings.UPDATE_LAST_LOGIN:
#             models.update_last_login(None, self.user)

#         return data
def get_token_for_user(user):
    refresh = RefreshToken(user)

    return {'refresh': str(refresh), 'access': str(refresh.access_token)}

class MyTok(TokenObtainSlidingSerializer):
    pass

class TokenSerializer(serializers.ModelSerializer):
    access_token = AccessToken()
    access = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()
    token_class = None
    
    class Meta:
        fields = ('username', 'confirmation_code', 'access', 'token')
        read_only_fields = ('access',)
        model = User
    
    def get_access(self, obj):
        print(self.access_token)
        return str(self.access_token)
    
    # @classmethod
    # def get_token(cls, user):
    #     return cls.token_class.for_user(user)

class Fuck(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["confirmation_code"] = serializers.CharField()
    
    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)
