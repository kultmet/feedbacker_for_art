from asyncio import constants
from secrets import choice
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


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

    role = models.CharField(max_length=15, choices=CHOICES, default='user')

    confirmation_code = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'username'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name="unique_fields"
            ),
        ]


    def __str__(self) -> str:
        return self.username
