from django.urls import path

from social_network.views import (
    PostListView
)

app_name = "social_network"

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
]
