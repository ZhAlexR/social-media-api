from rest_framework import serializers

from social_network.models import Post, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image"]

    def create(self, validated_data):
        post = self.context.get("post")
        image = validated_data.get("image")
        return Image.objects.create(image=image, post=post)


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["id", "title", "text", "created_at", "updated_at", "owner"]
        read_only_fields = ["id", "created_at", "updated_ad", "owner"]
