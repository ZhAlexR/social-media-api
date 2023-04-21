from django.urls import path, include
from rest_framework import routers

from user.views import ProfileViewSet, CreateUserView

route = routers.DefaultRouter()
route.register("profiles", ProfileViewSet,)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("", include(route.urls)),
]

app_name = "user"
