from email.mime import image
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


from .serializers import (
    UserSerializer,
    ConfirmationCodeSerializer,
    get_token_for_user,
    MyTokenObtainPairSerializer,
    MyObtenObtainSerializer

)
from .models import User
from .utility import generate_confirmation_code, send_email_with_verification_code

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = (permissions.IsAdminUser,)
    

@api_view(['GET', 'PATCH'])
def user_me(request):
    if request.method == 'PATCH':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, pk=request.user.pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)

# Нужно сделат валидацию по полю confirmation_code
# Нужно перехватить ошибку связаную с тем что юзер не существует
@api_view(['POST',])
def singup(request):
    data = {}
    data['email'] = request.data['email']
    data['username'] = request.data['username']
    username = request.data['username']
    email = request.data['email']
    print(request.data['username'])
    user = User.objects.get(username=username, email=email)
    data['confirmation_code'] = generate_confirmation_code()
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
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MyTokenObtainPairView(TokenObtainPairView):
    # serializer_class = MyTokenObtainPairSerializer
    serializer_class = MyObtenObtainSerializer


@api_view(['POST',])
def token(request):
    user = User.objects.get(username=request.data['username'], confirmation_code=request.data['confirmation_code'])
    # serializer = MyTokenObtainPairSerializer(user, request.data)
    # serializer = get_token_for_user(user)
    serializer = MyObtenObtainSerializer(user, request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     @csrf_exempt
# #

# @api_view(['POST',])
# def token(request):
#     for arg in ('username', 'confirmation_code'):
#         if not request.data.get(arg):
#             return Response(
#                 {arg: ["This field is required."]},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#     user = get_object_or_404(User, username=request.data['username'])
#     if request.data['confirmation_code'] == user.get_hash():
#         user.email_is_verified = True
#         user.save()
#         return Response(get_token_for_user(user), status=status.HTTP_200_OK)
#     return Response(
#         f'Confirmation code {request.data["confirmation_code"]} is  incorrect!'
#         ' Be sure to request it again',
#         status=status.HTTP_400_BAD_REQUEST
#     )