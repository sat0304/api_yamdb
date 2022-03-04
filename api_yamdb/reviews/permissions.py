from rest_framework import permissions

from users.models import User


class IsAdminOrSuperUser(permissions.BasePermission):
    """Права доступа для администратора"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff or request.user.role == User.admin:
            return True


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(request.user.is_staff or request.user.role == 'admin')


class ReviewCommentPermissions(permissions.BasePermission):
    """Права доступа для комментариев и отзывов"""
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return not request.user.is_anonymous()

        if request.method in ('PATCH', 'DELETE'):
            return (request.user == obj.author or
                    request.user.role == User.admin or
                    request.user.role == User.moderator)
        if request.method in permissions.SAFE_METHODS:
            return True
        return False
