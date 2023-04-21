from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import ProfileViewSet, CreateUserView

route = routers.DefaultRouter()
route.register("profiles", ProfileViewSet,)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("", include(route.urls)),
]

app_name = "user"
