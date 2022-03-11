from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdminOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(request.user.is_staff or request.user.role == 'admin')


class OwnerOrReadOnly(permissions.BasePermission):
   
    def has_object_permission(self, request, view, obj):
            return (self.request.user.role== 'admin'
                    or request.method in permissions.SAFE_METHODS)
