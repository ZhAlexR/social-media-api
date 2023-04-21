from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets

from user.models import Profile
from user.serializers import (
    ProfileListSerializer,
    UserSerializer,
    ProfileDetailSerializer
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileDetailSerializer

    def get_object(self):
        return self.request.user.profile


class ProfileViewSet(
    generics.ListAPIView,
    generics.RetrieveAPIView,
    viewsets.GenericViewSet
):
    queryset = Profile.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        return ProfileDetailSerializer
