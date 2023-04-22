from rest_framework import viewsets

from social_network.models import Post
from social_network.permissions import IsOwnerOrReadOnly
from social_network.serializers import PostSerializer


class PostViewSet(
    viewsets.ModelViewSet
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
