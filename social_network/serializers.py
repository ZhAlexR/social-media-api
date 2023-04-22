from rest_framework import serializers

from social_network.models import Post, Image, Tag


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


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["id", "title", "tags", "text", "created_at", "updated_at", "owner"]
        read_only_fields = ["id", "tags", "created_at", "updated_ad", "owner"]
