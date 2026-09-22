from rest_framework.permissions import BasePermission

from accounts.models import User


class IsOwner(BasePermission):
    message = "Only owners can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.OWNER
        )