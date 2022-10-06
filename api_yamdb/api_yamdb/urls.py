from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import singup, token, MyTokenObtainPairView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/', include('users.urls')),
    path('api/v1/auth/singup/', singup, name='singup'),
    # path('api/v1/auth/token/', TokenObtainPairView, name='token')
    # path('api/v1/auth/token/', MyTokenObtainPairView, name='token'),
    path('api/v1/auth/token/', token, name='token')
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)