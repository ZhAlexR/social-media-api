from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets

from user.models import Profile
from user.serializers import (
    ProfileListSerializer,
    UserSerializer,
    ProfileDetailSerializer,
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileDetailSerializer

    def get_object(self):
        return self.request.user.profile


class ProfileViewSet(
    generics.ListAPIView, generics.RetrieveAPIView, viewsets.GenericViewSet
):
    def get_queryset(self):
        queryset = Profile.objects.all()

        username = self.request.query_params.get("username")
        bio = self.request.query_params.get("bio")

        if username:
            queryset = queryset.filter(user__username__icontains=username)

        if bio:
            queryset = queryset.filter(bio__icontains=bio)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        return ProfileDetailSerializer
