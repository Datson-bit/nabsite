from django.urls import path
from .views import UserResgisterView

urlpatterns = [
    path('register/', UserResgisterView.as_view(), name="register")
]
