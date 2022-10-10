from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    ProfileViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
    UserViewSet,
    user_me,
    SignupView,
    SignUpViewSet,
    token
)


app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                   CommentViewSet,
                   basename='comments')
v1_router.register(r'users', UserViewSet, basename='users')
v1_router.register(r'auth/signup', SignUpViewSet)
# v1_router.register(r'users/me/', ProfileViewSet, basename='me')
# v1_router.register(r'users/me', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(v1_router.urls)),

    # path('users/me/', user_me, name='me'),
    # path('auth/signup/', signup, name='signup'),
    # path('auth/signup/', SignUpViewSet),
    # path('auth/signup/', SignupView.as_view(), name='signup'),
    #path('users/me/', user_me, name='user_me'),
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', token, name='token'),
]
