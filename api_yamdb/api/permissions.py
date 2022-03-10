from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_staff