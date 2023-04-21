from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from user.models import Profile
from user.serializers import ProfileSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

