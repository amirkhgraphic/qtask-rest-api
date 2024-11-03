from rest_framework import permissions


class IsOwnerOrAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow users to edit, view or delete their own account.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff

    def has_permission(self, request, view):
        return request.user.is_authenticated
