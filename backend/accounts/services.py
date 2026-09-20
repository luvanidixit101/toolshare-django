from django.db import transaction
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)


@transaction.atomic
def change_user_password(*, user, new_password):
    user.set_password(new_password)
    user.save(update_fields=["password"])

    outstanding_tokens = OutstandingToken.objects.filter(user=user)

    for token in outstanding_tokens:
        BlacklistedToken.objects.get_or_create(token=token)

    return user