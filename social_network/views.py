from django.db.models import Q, QuerySet
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)
from rest_framework import viewsets, status, generics
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="tag",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter posts by tag ids (coma separated)",
                examples=[
                    OpenApiExample("Empty tags", value=""),
                    OpenApiExample("Single tags", value=1),
                    OpenApiExample("Multiple tags", value="1,2"),
                ],
            ),
            OpenApiParameter(
                name="reaction",
                type={"type": "number"},
                description="Filter posts by user reaction id",
                examples=[
                    OpenApiExample("Empty reaction", value=""),
                    OpenApiExample("Filled reaction", value=1),
                ],
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        List all posts or filter by tags and reactions.

        Parameters:
        - `tag` (list[int]): Filter posts by tag ids (comma separated).
        - `reaction` (int): Filter posts by user reaction id.

        Example responses:
        - 200 OK: List of posts with applied filters.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        request=PostSerializer,
        responses={
            200: PostDetailSerializer,
            400: "Bad Request",
            401: "Unauthorized",
        },
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new post.

        Example responses:
        - 200 OK: Detailed representation of created post.
        - 400 Bad Request: Invalid data provided in the request.
        - 401 Unauthorized: User is not authenticated.
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(
        request=PostSerializer,
        responses={
            200: PostDetailSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
        },
    )
    def update(self, request, *args, **kwargs):
        """
        Update a post by ID.

        Example responses:
        - 200 OK: Detailed representation of updated post.
        - 400 Bad Request: Invalid data provided in the request.
        - 401 Unauthorized: User is not authenticated.
        - 403 Forbidden: User does not have permission to update this post.
        - 404 Not Found: Post with specified ID does not exist.
        """
        return super().update(request, *args, **kwargs)

    @extend_schema(
        request=PostSerializer,
        responses={
            200: PostDetailSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
        },
    )
    def destroy(self, request, *args, **kwargs):
        """
        Destroy the post with the specified ID.

        Example responses:
        - 204 No Content: Post successfully deleted.
        - 401 Unauthorized: User is not authenticated.
        - 403 Forbidden: User does not have permission to delete this post.
        - 404 Not Found: Post with specified ID does not exist.
        """
        return super().destroy(request, *args, **kwargs)

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


@extend_schema(
    description="Toggle a like reaction on a post.",
)
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


@extend_schema(
    description="Toggle a dislike reaction on a post.",
)
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
