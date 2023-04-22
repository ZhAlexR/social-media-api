from django.db.models import Q
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from social_network.models import Post, Tag
from social_network.permissions import IsOwnerOrReadOnly
from social_network.serializers import PostSerializer, ImageSerializer, TagSerializer


class PostViewSet(
    viewsets.ModelViewSet
):
    queryset = Post.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.filter(
            Q(owner=self.request.user)
            | Q(owner__in=self.request.user.following.all())
        )
        return queryset

    def get_serializer_class(self):
        if self.action == "upload_image":
            return ImageSerializer

        return PostSerializer

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request: Request, pk: int = None) -> Response:
        post = self.get_object()
        serializer = self.get_serializer(data=request.data, context={"post": post})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save()


class CreateTagView(generics.CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

