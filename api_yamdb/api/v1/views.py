from rest_framework import viewsets, permissions, mixins, status, filters, views
from rest_framework.generics import get_object_or_404
# from rest_framework.routers
from rest_framework import filters
from django.db.models import Avg

from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializerRead,
    TitleSerializerCreate,
    ReviewSerializer,
    CommentSerializer,
    ConfirmationCodeSerializer,
    UserSerializer,
    # get_token_for_user,
)
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User
from .utility import generate_confirmation_code, send_email_with_verification_code

from .permissions import (IsAuthorOrModeratorOrAdminOrReadOnly,
                          IsAdminOrSuperuserPermission,
                          IsAdminOrReadOnly,
                          TitleIsAdminOrReadOnly)


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
    # queryset = Title.objects.all().annotate(
    #     rating=Avg('reviews__score')
    # ).order_by('name')
    queryset = Title.objects.all().order_by('name')
    serializer_class = TitleSerializerCreate
    permission_classes = (TitleIsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'year', 'genre__slug', 'category__slug']

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE',):
            return TitleSerializerCreate
        return TitleSerializerRead


class CategoryViewSet(CreateDestroyViewSet):
    """Вьюсет для работы с категориями"""
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['slug']


class GenreViewSet(CreateDestroyViewSet):
    """Вьюсет для работы с жанрами"""
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['slug']


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами"""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями"""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'],
                                   title=self.kwargs['title_id']
                                   )
        serializer.save(author=self.request.user, review=review)


# Часть Димы


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('username')
    # permission_classes = (permissions.IsAdminUser,)
    permission_classes = (IsAdminOrSuperuserPermission,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

# это нужно будет обработать
    @action(
        detail=False,
        url_path='me',
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated,],
        queryset = User.objects.all()
    )
    def my(self, request):

        user = get_object_or_404(User, id=request.user.id)

        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)

        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)


@api_view(['GET', 'PATCH'])
def user_me(request):
    if request.method == 'PATCH':
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
class SignupView(views.APIView):

    def post(self, request):
        data = {}
        data['email'] = request.data.get('email')
        data['username'] = request.data.get('username')
        username = request.data.get('username')
        email = request.data.get('email')
        data['confirmation_code'] = generate_confirmation_code()
        # user = get_object_or_404(User, id=re)
        # user = User.objects.get(username=username, email=email)
        serializer = ConfirmationCodeSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            send_email_with_verification_code(serializer.data)
            return Response(
                {
                    'email': email,
                    'username': username
                }, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        data = {}
        data['email'] = request.data.get('email')
        data['username'] = request.data.get('username')
        username = request.data.get('username')
        email = request.data.get('email')
        data['confirmation_code'] = generate_confirmation_code()
        user = User.objects.get(username=username, email=email)
        serializer = ConfirmationCodeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            send_email_with_verification_code(serializer.data)
            return Response(
                {
                    'email': email,
                    'username': username
                }, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PATCH'])
def signup(request):
    data = {}
    data['email'] = request.data.get('email')
    data['username'] = request.data.get('username')
    username = request.data.get('username')
    email = request.data.get('email')
    data['confirmation_code'] = generate_confirmation_code()
    # print(request.data['username'])
    if request.method == 'PATCH':
        user = User.objects.get(username=username, email=email)
        serializer = ConfirmationCodeSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            send_email_with_verification_code(serializer.data)
            return Response(
                {
                    'email': email,
                    'username': username
                }, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        # if request.data['username'] != 'me':
        serializer = ConfirmationCodeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            send_email_with_verification_code(serializer.data)
            return Response(
                {
                    'email': email,
                    'username': username
                }, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SignUpViewSet(viewsets.):
class SignUpViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ConfirmationCodeSerializer

    def create(self, request, *args, **kwargs):
        data = {}
        data['email'] = request.data.get('email')
        data['username'] = request.data.get('username')
        username = request.data.get('username')
        email = request.data.get('email')
        data['confirmation_code'] = generate_confirmation_code()
        # user = User.objects.get(username=username, email=email)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        send_email_with_verification_code(data)
        try:
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        except KeyError:
            Response({'confirmation_code': 'Беда с ключами'}, headers=headers)

    def update(self, request, *args, **kwargs):
        data = {}
        data['email'] = request.data.get('email')
        data['username'] = request.data.get('username')
        username = request.data.get('username')
        email = request.data.get('email')
        data['confirmation_code'] = generate_confirmation_code()
        user = User.objects.get(username=request.data.get('username'), email=request.data.get('email'))
        serializer = self.get_serializer(user, data=data)
        headers = self.get_success_headers(serializer.data)
        send_email_with_verification_code(data)
        return Response(serializer.initial_data, status=status.HTTP_200_OK, headers=headers)


@api_view(['POST', ])
def token(request):
    user = User.objects.get(username=request.data.get('username'),
                            confirmation_code=request.data.get('confirmation_code'))

    token = get_tokens_for_user(user)
    return Response(token)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        # 'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
