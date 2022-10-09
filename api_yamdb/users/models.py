from asyncio import constants
from secrets import choice
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


# class UserManager(UserManager):
#     def create_user(self, username, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    CHOICES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
    )
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(
        verbose_name='email адрес',
        max_length=255,
        unique=True
    )
    bio = models.TextField(blank=True, null=True)
    # role = models.PositiveSmallIntegerField(choices=CHOICES, default=1)
    role = models.CharField(max_length=15, choices=CHOICES, default='user')
    confirmation_code = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'username'
    # CONFIRMATION_CODE_FIELD = 'confirmation_code'
    # REQUIRED_FIELDS = []
    # constants = [

    # ]

    # def is_admin(self):
    #     if self.
    def __str__(self) -> str:
        return self.username
