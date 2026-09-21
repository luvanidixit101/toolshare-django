from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
    )

    password_confirm = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
    )

    role = serializers.ChoiceField(
        choices=(
            User.Role.USER,
            User.Role.OWNER,
        ),
        default=User.Role.USER,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "password",
            "password_confirm",
        )
        read_only_fields = ("id",)

    def validate_email(self, value):
        email = value.strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return email

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm", None)

        if password != password_confirm:
            raise serializers.ValidationError(
                {
                    "password_confirm": (
                        "Password and confirmation password do not match."
                    )
                }
            )

        try:
            validate_password(password)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                {"password": list(exc.messages)}
            ) from exc

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data,
        )

        return user




class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = {
            "id": self.user.id,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "role": self.user.role,
        }

        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)

    def validate_refresh(self, value):
        try:
            token = RefreshToken(value)
            token.blacklist()
        except TokenError as exc:
            raise serializers.ValidationError(
                "Invalid or expired refresh token."
            ) from exc

        return value
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "date_joined",
        )
        read_only_fields = fields


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
        )

    def validate_first_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "First name cannot be empty."
            )

        return value

    def validate_last_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Last name cannot be empty."
            )

        return value


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
    )

    new_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
    )

    new_password_confirm = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
    )

    def validate(self, attrs):
        user = self.context["request"].user

        current_password = attrs["current_password"]
        new_password = attrs["new_password"]
        new_password_confirm = attrs["new_password_confirm"]

        if not user.check_password(current_password):
            raise serializers.ValidationError(
                {
                    "current_password": (
                        "Current password is incorrect."
                    )
                }
            )

        if new_password != new_password_confirm:
            raise serializers.ValidationError(
                {
                    "new_password_confirm": (
                        "New password and confirmation password do not match."
                    )
                }
            )

        if user.check_password(new_password):
            raise serializers.ValidationError(
                {
                    "new_password": (
                        "New password must be different from the current password."
                    )
                }
            )

        try:
            validate_password(
                new_password,
                user=user,
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                {
                    "new_password": list(exc.messages)
                }
            ) from exc

        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value.strip().lower()




class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    new_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
    )

    new_password_confirm = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
    )

    def validate(self, attrs):
        uid = attrs["uid"]
        new_password = attrs["new_password"]
        new_password_confirm = attrs["new_password_confirm"]

        if new_password != new_password_confirm:
            raise serializers.ValidationError(
                {
                    "new_password_confirm": (
                        "New password and confirmation password do not match."
                    )
                }
            )

        try:
            user_id = force_str(
                urlsafe_base64_decode(uid)
            )

            user = User.objects.get(
                pk=user_id,
                is_active=True,
            )

        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
        ) as exc:
            raise serializers.ValidationError(
                {
                    "token": "Invalid or expired password reset link."
                }
            ) from exc

        try:
            validate_password(
                new_password,
                user=user,
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                {
                    "new_password": list(exc.messages)
                }
            ) from exc

        attrs["user"] = user

        return attrs