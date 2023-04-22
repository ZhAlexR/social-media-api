from rest_framework import serializers

from social_network.models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["id", "title", "images", "text", "created_at", "updated_at", "owner"]
        read_only_fields = ["id", "created_at", "updated_ad", "owner"]
