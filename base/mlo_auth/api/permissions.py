from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS
)


class IsStaffOrReadOnly(BasePermission):
    """
    Права для редактирования данных пользователей предоставляются только пользователям is_staff=True
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user.is_staff
        )
