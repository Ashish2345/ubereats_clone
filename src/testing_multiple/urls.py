from django.urls import path
from .views import *

urlpatterns = [
    path("", Testing.as_view(),name="test")
]
