from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

class OwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
            return (self.request.user.role== 'admin'
                    or request.method in permissions.SAFE_METHODS)