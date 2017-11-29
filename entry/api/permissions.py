from django.utils.translation import ugettext_lazy as _
from rest_framework.permissions import BasePermission


class IsOwnerOrStaffOrReadOnly(BasePermission):
    message = _('Для редактирования вы должны быть администратором или автором вопроса.')

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.author == request.user
