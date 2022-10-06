from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CHOICES = (
    (1, 'user'),
    (2, 'moderator'),
    (3, 'admin'),
    )
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(
        verbose_name='email адрес',
        max_length=255,
        unique=True
    )
    bio = models.TextField(blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=CHOICES, default=1)
    confirmation_code = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=255,blank=True, null=True)

    CONFIRMATION_CODE_FIELD = 'confirmation_code'
    
    
    def __str__(self) -> str:
        return self.username


# class ConfirmationCode(models.Model):
#     email = models.EmailField()
#     user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
#     confirmation_code = models.IntegerField(blank=True, null=True)