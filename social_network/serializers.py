from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from social_network.models import Post, Image, Tag, Comment


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image"]

    def create(self, validated_data):
        post = self.context.get("post")
        image = validated_data.get("image")
        return Image.objects.create(image=image, post=post)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name", "post"]


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "text",
            "owner",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "created_at",
            "updated_at",
        ]


class CommentDetailSerializer(CommentSerializer):
    class Meta(CommentSerializer.Meta):
        read_only_fields = CommentSerializer.Meta.read_only_fields.append(
            "post"
        )


class CommentPostDetailSerializer(CommentSerializer):
    class Meta(CommentSerializer.Meta):
        fields = [
            "id",
            "text",
            "owner",
            "created_at",
            "updated_at",
        ]


class PostSerializer(serializers.ModelSerializer):
    text_preview = serializers.SerializerMethodField()
    owner = serializers.SlugRelatedField(slug_field="username", read_only=True)
    tags = serializers.SlugRelatedField(
        many=True, slug_field="name", read_only=True
    )

    reactions = serializers.SerializerMethodField(
        method_name="reaction_counts", read_only=True
    )
    comment_number = serializers.SerializerMethodField(
        method_name="comment_count", read_only=True
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "tags",
            "text_preview",
            "created_at",
            "owner",
            "reactions",
            "comment_number",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]

    @staticmethod
    def reaction_counts(obj) -> dict:
        likes_count = obj.reactions.filter(reaction="LIKE").count()
        dislikes_count = obj.reactions.filter(reaction="DIS").count()
        return {"likes": likes_count, "dislikes": dislikes_count}

    @staticmethod
    def comment_count(obj) -> int:
        return obj.comments.count()

    @staticmethod
    def get_text_preview(obj) -> str:
        return obj.text[:50] + " ..."


class PostDetailSerializer(PostSerializer):
    comments = CommentPostDetailSerializer(many=True, read_only=True)

    class Meta(PostSerializer.Meta):
        fields = [
            "id",
            "title",
            "text",
            "tags",
            "created_at",
            "updated_at",
            "owner",
            "reactions",
            "comment_number",
            "comments",
        ]
