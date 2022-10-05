from rest_framework import viewsets, permissions, mixins
from rest_framework.generics import get_object_or_404
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser

from .serializers import (
    ReviewSerializer,
    CommentSerializer,
    TitleSerializer)
from reviews.models import Review, Comment, Title
# from .permissions import AuthorOrModeratorOrAdminOrReadOnly


# @api_view(['GET'])
# @permission_classes([AllowAny])
class TitleViewSet(viewsets.ModelViewSet):      # временно
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = (IsAdminUser,)

# @api_view(['GET'])
# @permission_classes([AllowAny])
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (AuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


# @api_view(['GET'])
# @permission_classes([AllowAny])
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = (AuthorOrModeratorOrAdminOrReadOnly,)
    # pagination_class = None

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
