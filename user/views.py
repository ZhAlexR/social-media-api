from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.request import Request
from rest_framework.response import Response

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
    generics.ListAPIView,
    generics.RetrieveAPIView,
    viewsets.GenericViewSet
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


@api_view(["GET"])
def toggle_follow(request: Request, pk: int) -> Response:
    current_user = request.user
    toggle_follow_user = get_object_or_404(get_user_model(), pk=pk)

    if current_user in toggle_follow_user.followers.all():
        toggle_follow_user.followers.remove(current_user)
    else:
        toggle_follow_user.followers.add(current_user)
    return Response(status=status.HTTP_200_OK)
