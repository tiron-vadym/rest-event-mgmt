from django.urls import path

from users.views import UserSignupView

urlpatterns = [
    path("", UserSignupView.as_view(), name="user-signup"),
]
