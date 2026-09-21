from django.conf import settings
from django.core import signing


EMAIL_VERIFICATION_SALT = "accounts.email-verification"


def generate_email_verification_token(user):
    payload = {
        "user_id": user.pk,
        "email": user.email,
    }

    return signing.dumps(
        payload,
        salt=EMAIL_VERIFICATION_SALT,
    )


def verify_email_verification_token(token):
    try:
        payload = signing.loads(
            token,
            salt=EMAIL_VERIFICATION_SALT,
            max_age=settings.EMAIL_VERIFICATION_TIMEOUT,
        )
    except (
        signing.SignatureExpired,
        signing.BadSignature,
    ):
        return None

    return payload