from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView

from social_network.models import Post
from social_network.serializers import PostSerializer


class PostListView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
