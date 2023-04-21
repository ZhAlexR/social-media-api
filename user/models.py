from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    photo = models.ImageField(upload_to=f"profiles/{user.username}")
    bio = models.TextField()

    def __str__(self) -> str:
        return f"profile{self.id} ({self.user.username})"
