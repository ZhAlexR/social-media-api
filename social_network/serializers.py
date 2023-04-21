from rest_framework import serializers

from social_network.models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["title", "text", "created_at", "updated_at", "owner"]
        read_only_fields = ["created_at", "updated_ad"]
