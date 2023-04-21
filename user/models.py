import os
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    pass


def create_photo_path(instance, filename: str) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.user.username)}-{uuid.uuid4()}{extension}"
    return os.path.join(f"profiles/{instance.user.username}{instance.user.pk}", filename)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    photo = models.ImageField(upload_to=create_photo_path,
                              null=True, blank=True)
    bio = models.TextField()

    def __str__(self) -> str:
        return f"profile{self.id} ({self.user})"
