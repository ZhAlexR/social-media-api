from django.urls import path, include
from rest_framework import routers

from social_network.views import (
    PostViewSet,
    CreateTagView,
    toggle_like,
    toggle_dislike,
    CommentViewSet,
)
from user.views import ProfileViewSet

app_name = "social_network"

route = routers.DefaultRouter()
route.register("profiles", ProfileViewSet, basename="profile")
route.register("posts", PostViewSet, basename="post")
route.register("comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("tags/create", CreateTagView.as_view(), name="tag-create"),
    path("toggle-like/post/<int:pk>/", toggle_like, name="toggle-like"),
    path(
        "toggle-dislike/post/<int:pk>/", toggle_dislike, name="toggle-dislike"
    ),
    path("", include(route.urls)),
]
