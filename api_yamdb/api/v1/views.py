from rest_framework import viewsets, permissions, mixins, status, filters
from rest_framework.generics import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination

# from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializerRead,
    TitleSerializerCreate,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    ConfirmationCodeSerializer,
    # get_token_for_user,
    MyTokenObtainPairSerializer,
    MyObtainSerializer,
    TokenSerializer,
    Fuck
)
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User
from .utility import generate_confirmation_code, send_email_with_verification_code
# from .permissions import AuthorOrModeratorOrAdminOrReadOnly
from .permissions import IsAdminOrReadOnly


class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


# @api_view(['GET'])
# @permission_classes([AllowAny])
class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializerCreate
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'year', 'genre__slug', 'category__slug']

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE',):
            return TitleSerializerCreate
        return TitleSerializerRead

    # def perform_create(self, serializer):
    #     t = 0



class CategoryViewSet(CreateDestroyViewSet):
    """Вьюсет для работы с категориями"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['slug']


class GenreViewSet(CreateDestroyViewSet):
    """Вьюсет для работы с жанрами"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['slug']


# @api_view(['GET'])
# @permission_classes([AllowAny])
class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами"""
    serializer_class = ReviewSerializer
    # permission_classes = (AuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        print('$$$$$$$$$$$$$$$$')
        print(self.kwargs['title_id'])
        print(self.kwargs.get('title_id'))
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        print('!!!!!!!!!!!!!!!')
        print(title)
        user = self.request.user
        print(self.request)
        print(self.get_queryset(id='user'))
        print(user)
        print(user.id)
        return title.reviews.all()

    def perform_create(self, serializer):
        print('&&&&&&&&&&&&&&&&')
        print(self.request.user_id)
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


# @api_view(['GET'])
# @permission_classes([AllowAny])
class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями"""
    serializer_class = CommentSerializer
    # permission_classes = (AllowAny,)
    # permission_classes = (AuthorOrModeratorOrAdminOrReadOnly,)
    # pagination_class = None

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        print('@@@@@@@@@@@@@@@@@@@@@@@@')
        print(title_id)
        print(review_id)
        print(self.request.user)
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author_id=self.request.user, review=review)


# Часть Димы


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAdminUser,)
    

@api_view(['GET', 'PATCH'])
def user_me(request):
    if request.method == 'PATCH':
        print()
        user = get_object_or_404(User, pk=request.user.pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, pk=request.user.pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)

# Нужно сделат валидацию по полю confirmation_code
# Нужно перехватить ошибку связаную с тем что юзер не существует
@api_view(['POST', 'PATCH'])
def signup(request):
    data = {}
    data['email'] = request.data['email']
    data['username'] = request.data['username']
    username = request.data['username']
    email = request.data['email']
    data['confirmation_code'] = generate_confirmation_code()
    print(request.data['username'])
    if request.method == 'PATCH':
        user = User.objects.get(username=username, email=email)
        serializer = ConfirmationCodeSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            send_email_with_verification_code(serializer.data)
            return Response(
                {
                    'ready': 
                    f'Код подтверждения был отправлен вам на почту {email}'
                }, status=status.HTTP_201_CREATED
            )
    elif request.method == 'POST':
        serializer = ConfirmationCodeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            send_email_with_verification_code(serializer.data)
            return Response(
                {
                    'ready': 
                    f'Код подтверждения был отправлен вам на почту {email}'
                }, status=status.HTTP_200_OK
            )



@api_view(['POST',])
def token(request):
    user = User.objects.get(username=request.data['username'], confirmation_code=request.data['confirmation_code'])
  
    token = get_tokens_for_user(user)
    return Response(token)




def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
