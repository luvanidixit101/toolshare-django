from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

from .models import User


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