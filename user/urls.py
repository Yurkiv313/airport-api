from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from user.views import (
    CreateUserView,
    ManageUserView,
    CustomTokenObtainPairView
)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("me/", ManageUserView.as_view(), name="manage_user"),
    path(
        "token/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

app_name = "user"
