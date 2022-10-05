from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import (
    ReviewViewSet,
    CommentViewSet,
    TitleViewSet,
)

v1_router = DefaultRouter()

v1_router.register(r'titles', TitleViewSet)
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                   CommentViewSet,
                   basename='comments')

urlpatterns = [
    path('', include(v1_router.urls)),
]
