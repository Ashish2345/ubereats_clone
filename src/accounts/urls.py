from django.urls import path

from .views import (UserAPIView, RegisterAPIView, LoginAPIView, RefreshAPIView, LogoutAPIView)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("user/", UserAPIView.as_view(), name="home"),
    path("refresh_token/", RefreshAPIView.as_view(), name="refresh"),
    path("logout/", LogoutAPIView.as_view(), name="logout")
]
