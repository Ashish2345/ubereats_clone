from django.urls import path

from .views import (HomeView, RegisterAPIView, LoginAPIView)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("home/", HomeView.as_view(), name="home")
]
