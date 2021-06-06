from rest_framework import permissions


class IsNotSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user.is_superuser or request.user.is_staff):
            return False
        return True
