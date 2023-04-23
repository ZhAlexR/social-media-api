from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet
from rest_framework import viewsets, status, generics, serializers
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.request import Request
from rest_framework.response import Response

from social_network.models import Post, Tag, Reaction, Comment
from social_network.permissions import IsOwnerOrReadOnly
from social_network.serializers import (
    PostSerializer,
    ImageSerializer,
    TagSerializer,
    PostDetailSerializer,
    CommentSerializer,
    CommentDetailSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @staticmethod
    def _params_to_digit_list(params: str) -> list[int]:
        return [int(param) for param in params.split(",")]

    def get_queryset(self):
        queryset = Post.objects.all()
        tags = self.request.query_params.get("tags")
        reaction = self.request.query_params.get("reaction")

        if self.request.user.is_authenticated:
            queryset = Post.objects.filter(
                Q(owner=self.request.user)
                | Q(owner__in=self.request.user.following.all())
            )

        if tags:
            queryset = queryset.filter(
                tags__in=self._params_to_digit_list(tags)
            ).distinct()

        if reaction:
            queryset = queryset.filter(reactions=reaction)
        return queryset

    def get_serializer_class(self):
        if self.action in ["retrieve", "update"]:
            return PostDetailSerializer

        if self.action == "upload_image":
            return ImageSerializer

        if self.action == "comment":
            return CommentSerializer

        return PostSerializer

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request: Request, pk: int = None) -> Response:
        post = self.get_object()
        serializer = self.get_serializer(
            data=request.data, context={"post": post}
        )

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
    permission_classes = [IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self) -> QuerySet:
        query = Comment.objects.filter(owner=self.request.user)
        return query

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CommentDetailSerializer
        return CommentSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def toggle_like(request: Request, pk: int) -> Response:
    current_user = request.user
    post = get_object_or_404(Post, pk=pk)

    try:
        reaction = Reaction.objects.get(post=post, owner=current_user)
        if reaction.reaction == "DIS":
            reaction.reaction = "LIKE"
            reaction.save()
            return Response({"status": "liked"}, status=status.HTTP_200_OK)
        reaction.delete()
        return Response(
            {"status": "reaction is deleted"}, status=status.HTTP_200_OK
        )
    except Reaction.DoesNotExist:
        reaction = Reaction(post=post, owner=current_user, reaction="LIKE")
        reaction.save()
        return Response({"status": "liked"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def toggle_dislike(request: Request, pk: int) -> Response:
    current_user = request.user
    post = get_object_or_404(Post, pk=pk)

    try:
        reaction = Reaction.objects.get(post=post, owner=current_user)
        if reaction.reaction == "LIKE":
            reaction.reaction = "DIS"
            reaction.save()
            return Response({"status": "disliked"}, status=status.HTTP_200_OK)
        reaction.delete()
        return Response(
            {"status": "reaction is deleted"}, status=status.HTTP_200_OK
        )
    except Reaction.DoesNotExist:
        reaction = Reaction(post=post, owner=current_user, reaction="DIS")
        reaction.save()
        return Response({"status": "disliked"}, status=status.HTTP_200_OK)
