import logging
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import (
    generate_email_verification_token,
    verify_email_verification_token,
)
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

from .models import User

logger = logging.getLogger(__name__)


@transaction.atomic
def change_user_password(*, user, new_password):
    user.set_password(new_password)
    user.save(update_fields=["password"])

    outstanding_tokens = OutstandingToken.objects.filter(user=user)

    for token in outstanding_tokens:
        BlacklistedToken.objects.get_or_create(token=token)

    return user


def request_password_reset(*, email):
    user = (
        User.objects
        .filter(
            email__iexact=email,
            is_active=True,
        )
        .first()
    )

    if user is None:
        return

    uid = urlsafe_base64_encode(
        force_bytes(user.pk)
    )

    token = default_token_generator.make_token(user)

    frontend_url = settings.FRONTEND_URL.rstrip("/")

    reset_url = (
        f"{frontend_url}/reset-password/"
        f"{uid}/{token}"
    )

    send_mail(
        subject="Reset your ToolShare password",
        message=(
            "We received a request to reset your ToolShare password.\n\n"
            f"Reset your password using this link:\n{reset_url}\n\n"
            "This link expires in 30 minutes.\n\n"
            "If you did not request a password reset, "
            "you can safely ignore this email."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )   


def confirm_password_reset(*, user, token, new_password):
    if not default_token_generator.check_token(
        user,
        token,
    ):
        return False

    change_user_password(
        user=user,
        new_password=new_password,
    )

    return True


def send_email_verification(*, user):
    if user.is_email_verified:
        return True

    token = generate_email_verification_token(user)

    frontend_url = settings.FRONTEND_URL.rstrip("/")

    verification_url = (
        f"{frontend_url}/verify-email"
        f"?token={token}"
    )

    try:
        send_mail(
            subject="Verify your ToolShare email",
            message=(
                f"Hello {user.first_name or 'ToolShare User'},\n\n"
                "Welcome to ToolShare.\n\n"
                "Please verify your email address using the link below:\n\n"
                f"{verification_url}\n\n"
                "This verification link expires in 24 hours.\n\n"
                "If you did not create this account, "
                "you can safely ignore this email."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception:
        logger.exception(
            "Failed to send verification email for user_id=%s",
            user.pk,
        )
        return False

    return True

@transaction.atomic
def verify_user_email(*, token):
    payload = verify_email_verification_token(token)

    if payload is None:
        return None

    user_id = payload.get("user_id")
    email = payload.get("email")

    if not user_id or not email:
        return None

    user = (
        User.objects
        .filter(
            pk=user_id,
            email__iexact=email,
            is_active=True,
        )
        .first()
    )

    if user is None:
        return None

    if user.is_email_verified:
        return user

    user.email_verified_at = timezone.now()

    user.save(
        update_fields=["email_verified_at"]
    )

    return user

def resend_email_verification(*, email):
    user = (
        User.objects
        .filter(
            email__iexact=email,
            is_active=True,
        )
        .first()
    )

    if user is None:
        return

    if user.is_email_verified:
        return

    send_email_verification(user=user)