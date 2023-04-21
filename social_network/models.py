import os
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    def __str__(self) -> str:
        return f"{self.title[:10]} by {self.owner.username}"


class Comment(models.Model):
    text = models.CharField(max_length=255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    def __str__(self) -> str:
        return f"{self.text[:10]} by {self.owner.username}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes"
    )


class Tag(models.Model):
    name = models.CharField(max_length=63)
    post = models.ManyToManyField(Post, related_name="tags")

    def __str__(self) -> str:
        return self.name


def create_image_path(instance, filename: str) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.user.username)}-{uuid.uuid4()}{extension}"
    return os.path.join(f"posts/post{instance.pk}", filename)


class Image(models.Model):
    image = models.ImageField(upload_to=create_image_path)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="images"
    )
