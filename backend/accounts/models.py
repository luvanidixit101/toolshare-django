from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = "USER", "User"
        OWNER = "OWNER", "Owner"
        ADMIN = "ADMIN", "Admin"

    username = None

    email = models.EmailField(
        unique=True,
        db_index=True,
    )

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
    )

    email_verified_at = models.DateTimeField(
    null=True,
    blank=True,
   )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def is_email_verified(self):
        return self.email_verified_at is not None

    def __str__(self):
        return self.email