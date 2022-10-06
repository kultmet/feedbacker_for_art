from django.contrib.auth import authenticate, models
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer, PasswordField
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserSerializer(serializers.ModelSerializer):
  
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class ConfirmationCodeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email', 'username', 'confirmation_code')
        model = User


class MyObtenObtainSerializer(TokenObtainSerializer):

    username_field = User().USERNAME_FIELD
    token_class = None

    default_error_messages = {
        "no_active_account": ("No active account found with the given credentials")
    }
    # class Meta:
    #     fields = ('username', 'confirmation_code')
        # extra_kwargs = {'password': {'required': False}}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["confirmation_code"] = serializers.IntegerField()
        self.fields['password'] = serializers.CharField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "confirmation_code": attrs["confirmation_code"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass
        self.user = authenticate(**authenticate_kwargs)
        return {}


class MyTokenObtainPairSerializer(MyObtenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            models.update_last_login(None, self.user)

        return data

# class MyTokenObtainPairSerializer(serializers.ModelSerializer):
#     token_class = RefreshToken


#     def validate(self, attrs):
#         data = super().validate(attrs)

#         refresh = self.get_token(self.user)

#         data["refresh"] = str(refresh)
#         data["access"] = str(refresh.access_token)

#         if api_settings.UPDATE_LAST_LOGIN:
#             models.update_last_login(None, self.user)

#         return data
def get_token_for_user(user):
    refresh = RefreshToken(user)

    return {'refresh': str(refresh), 'access': str(refresh.access_token)}

