# from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .services import (
    change_user_password,
    confirm_password_reset,
    request_password_reset,
    send_email_verification,
    verify_user_email,
    resend_email_verification,
)

from .serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    LogoutSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
    EmailVerificationSerializer,
    ResendEmailVerificationSerializer,
)

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        verification_email_sent = send_email_verification(
            user=user
        )

        return Response(
            {
                "message": (
                    "User registered successfully. "
                    "Please verify your email address."
                ),
                "verification_email_sent": verification_email_sent,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "is_email_verified": user.is_email_verified,
                },
            },
            status=status.HTTP_201_CREATED,
        )

class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = ()
    authentication_classes = () 



class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class MeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserProfileSerializer(request.user)

        return Response(
            {
                "user": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request):
        serializer = UserProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_serializer = UserProfileSerializer(
            request.user,
        )

        return Response(
            {
                "message": "Profile updated successfully.",
                "user": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        change_user_password(
            user=request.user,
            new_password=serializer.validated_data["new_password"],
        )

        return Response(
            {
                "message": (
                    "Password changed successfully. "
                    "Please login again."
                )
            },
            status=status.HTTP_200_OK,
        )


class PasswordResetRequestAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_password_reset(
            email=serializer.validated_data["email"]
        )

        return Response(
            {
                "message": (
                    "If an account exists with this email, "
                    "password reset instructions have been sent."
                )
            },
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        success = confirm_password_reset(
            user=serializer.validated_data["user"],
            token=serializer.validated_data["token"],
            new_password=serializer.validated_data[
                "new_password"
            ],
        )

        if not success:
            return Response(
                {
                    "token": [
                        "Invalid or expired password reset link."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": (
                    "Password reset successfully. "
                    "Please login with your new password."
                )
            },
            status=status.HTTP_200_OK,
        )
    
class EmailVerificationAPIView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        user = verify_user_email(
            token=serializer.validated_data["token"]
        )

        if user is None:
            return Response(
                {
                    "token": [
                        "Invalid or expired email verification link."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "Email verified successfully.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "is_email_verified": (
                        user.is_email_verified
                    ),
                    "email_verified_at": (
                        user.email_verified_at
                    ),
                },
            },
            status=status.HTTP_200_OK,
        )


class ResendEmailVerificationAPIView(generics.GenericAPIView):
    serializer_class = ResendEmailVerificationSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        resend_email_verification(
            email=serializer.validated_data["email"]
        )

        return Response(
            {
                "message": (
                    "If an unverified account exists with this email, "
                    "a verification link has been sent."
                )
            },
            status=status.HTTP_200_OK,
        )
# Create your views here.
