from django.urls import path, include
from rest_framework import routers

from social_network.views import PostViewSet, CreateTagView
from user.views import ProfileViewSet

app_name = "social_network"

route = routers.DefaultRouter()
route.register("profiles", ProfileViewSet, basename="profile")
route.register("posts", PostViewSet, basename="post")

urlpatterns = [
    path("tags/create", CreateTagView.as_view(), name="tag-create"),
    path("", include(route.urls)),
]
