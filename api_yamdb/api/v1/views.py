from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, permissions, mixins, status
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, Review
from users.models import User
from .filters import TitleFilter
from .permissions import (
    IsAdminOrSuperuserPermission,
    TitlePermission,
    ReviewPermission
)
from .serializers import (
    AdminUserSerializer,
    CategorySerializer,
    CommentSerializer,
    ConfirmationCodeSerializer,
    GenreSerializer,
    TitleSerializerRead,
    TitleSerializerCreate,
    ReviewSerializer,
    TokenSerializer,
    UserSerializer,
)
from .utility import generate_confirmation_code, send_email_with_verification_code


class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями"""
    queryset = Title.objects.all().order_by('name')
    serializer_class = TitleSerializerCreate
    permission_classes = (TitlePermission,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE',):
            return TitleSerializerCreate
        return TitleSerializerRead


class CategoryViewSet(CreateDestroyViewSet):
    """Вьюсет для работы с категориями"""
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = (TitlePermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyViewSet):
    """Вьюсет для работы с жанрами"""
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    permission_classes = (TitlePermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами"""
    serializer_class = ReviewSerializer
    permission_classes = (ReviewPermission,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями"""
    serializer_class = CommentSerializer
    permission_classes = (ReviewPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'],
                                   title=self.kwargs['title_id']
                                   )
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdminOrSuperuserPermission,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_serializer_class(self):
        if self.request.user.role != 'admin' or self.request.user.is_superuser:
            return UserSerializer
        return AdminUserSerializer

    @action(
        detail=False,
        url_path='me',
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated, ],
        queryset=User.objects.all()
    )
    def me(self, request):
        user = get_object_or_404(User, id=request.user.id)
        if request.method == 'PATCH':

            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)

        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', 'PATCH'])
def signup(request):
    data = {}
    data['email'] = request.data.get('email')
    data['username'] = request.data.get('username')
    username = request.data.get('username')
    email = request.data.get('email')
    data['confirmation_code'] = generate_confirmation_code()
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


class SignUpViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ConfirmationCodeSerializer

    def create(self, request, *args, **kwargs):
        data = {}
        data['email'] = request.data.get('email')
        data['username'] = request.data.get('username')
        data['confirmation_code'] = generate_confirmation_code()
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
        data['confirmation_code'] = generate_confirmation_code()
        user = User.objects.get(username=request.data.get('username'), email=request.data.get('email'))
        serializer = self.get_serializer(user, data=data)
        send_email_with_verification_code(data)
        return Response(serializer.initial_data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = TokenSerializer

    def get_queryset(self):
        return get_object_or_404(
            User, username=self.request.data.get('username')
        )

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        if username is None:
            return Response({"fail": "Нельзя без username"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = get_object_or_404(User, username=username)
        except Exception:
            return Response({"not_found": "нет такого"}, status=status.HTTP_404_NOT_FOUND)
        if request.data.get('confirmation_code') == user.confirmation_code:
            serializer = self.get_serializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'bad_request': 'confirmation_code invalid', }, status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }
