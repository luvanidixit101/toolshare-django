from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView 

from .views import (
    ChangePasswordAPIView,
    LoginAPIView,
    LogoutAPIView,
    MeAPIView,
    PasswordResetConfirmAPIView,
    PasswordResetRequestAPIView,
    RegisterAPIView,
    EmailVerificationAPIView,
    ResendEmailVerificationAPIView,
)


app_name = "accounts"

urlpatterns = [
    path(
        "register/",
        RegisterAPIView.as_view(),
        name="register",
    ),
    path(
        "login/",
        LoginAPIView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        LogoutAPIView.as_view(),
        name="logout",

    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),
    path(
        "me/",
        MeAPIView.as_view(),
        name="me",
    ),
    path(
        "change-password/",
        ChangePasswordAPIView.as_view(),
        name="change-password",
    ),

    path(
        "password-reset/request/",
        PasswordResetRequestAPIView.as_view(),
         name="password-reset-request",
    ),

    path(
    "password-reset/confirm/",
    PasswordResetConfirmAPIView.as_view(),
    name="password-reset-confirm",
    ),

   path(
       "verify-email/",
       EmailVerificationAPIView.as_view(),
       name="verify-email",
   ),

   path(
    "verify-email/resend/",
    ResendEmailVerificationAPIView.as_view(),
    name="verify-email-resend",
   ),
]