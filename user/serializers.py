from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from user.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "password", "is_staff"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        password = validated_data.get("password")
        if password:
            instance.set_password(password)
        instance.email = validated_data.get("email", instance.email)
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "photo", "bio"]


class ProfileListSerializer(ProfileSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta(ProfileSerializer.Meta):
        fields = ["id", "username", "photo", "bio"]


class ProfileDetailSerializer(ProfileSerializer):
    username = serializers.CharField(source="user.username")

    class Meta(ProfileSerializer.Meta):
        fields = ["id", "username", "photo", "bio"]

    def update(self, instance, validated_data):
        instance.user.username = validated_data.get("user").get("username", instance.user.username)
        instance.user.save()
        instance.bio = validated_data.get("bio", instance.bio)
        instance.photo = validated_data.get("bio", instance.photo)
        instance.save()
        return instance
