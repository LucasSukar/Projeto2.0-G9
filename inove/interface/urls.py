from django.urls import path
from .views import ScreenView

urlpatterns = [
    path("", ScreenView.as_view(), name = 'face'),
]