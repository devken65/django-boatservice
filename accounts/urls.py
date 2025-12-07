from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import ChangePassword, JWTLogIn, LogIn, LogOut, Me, PublicUser, Users

urlpatterns = [
    path("", Users.as_view()),
    path("me", Me.as_view()),
    path("change-password", ChangePassword.as_view()),
    # Cookie Login with username, password
    path("log-in", LogIn.as_view()),
    path("log-out", LogOut.as_view()),
    # auth Token with username, password
    path("token-login", obtain_auth_token),
    # JWT Login with username, password
    path("jwt-login", JWTLogIn.as_view()),
    path("@<str:username>", PublicUser.as_view()),
]
