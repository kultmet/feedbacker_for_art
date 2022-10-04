from rest_framework import viewsets, permissions, mixins
from rest_framework import filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from .serializers import (
    ReviewSerializer,
    CommentSerializer)
from reviews.models import Review, Comment, Title
# from .permissions import AuthorOwnerOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    # queryset = Post.objects.select_related('author', )
    # serializer_class = PostSerializer
    # permission_classes = (
    #     IsAuthenticatedOrReadOnly,
    #     AuthorOwnerOrReadOnly,
    # )
    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    # serializer_class = CommentSerializer
    # permission_classes = (
    #     IsAuthenticatedOrReadOnly,
    #     AuthorOwnerOrReadOnly,
    # )
    # pagination_class = None
    #
    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)
