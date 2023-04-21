from django.urls import path, include
from rest_framework import routers

from social_network.views import (
    PostListView
)
from user.views import ProfileViewSet

app_name = "social_network"

route = routers.DefaultRouter()
route.register("profiles", ProfileViewSet,)

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("", include(route.urls)),
]
