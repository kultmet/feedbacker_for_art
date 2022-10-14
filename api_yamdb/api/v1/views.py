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


class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями."""
    queryset = Title.objects.all().order_by('name')
    serializer_class = TitleSerializerCreate
    permission_classes = (TitlePermission,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE',):
            return TitleSerializerCreate
        return TitleSerializerRead


class CategoryViewSet(CreateDestroyViewSet):
    """Вьюсет для работы с категориями."""
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = (TitlePermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyViewSet):
    """Вьюсет для работы с жанрами."""
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    permission_classes = (TitlePermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами."""
    serializer_class = ReviewSerializer
    permission_classes = (ReviewPermission,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""
    serializer_class = CommentSerializer
    permission_classes = (ReviewPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    """Работа с пользователями. Только для администратора."""
    queryset = User.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrSuperuserPermission,
    )
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_serializer_class(self):
        if (
            self.request.user.role != 'admin'
            or self.request.user.is_superuser
        ):
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
        """
        Профиль пользователя. Можно редактировать.
        Поле role редактирует только администратор.
        """
        user = get_object_or_404(User, id=request.user.id)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignUpViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """Регистрация нового пользователя. Полечуние кода подтверждения."""
    queryset = User.objects.all()
    serializer_class = ConfirmationCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )


@api_view(http_method_names=['POST', ])
def token(request):
    """Выдает токен авторизации."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    user = get_object_or_404(User, **data)
    refresh = RefreshToken.for_user(user)
    return Response(
        {'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED
    )
