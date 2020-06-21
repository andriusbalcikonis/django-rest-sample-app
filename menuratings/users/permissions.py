from rest_framework import permissions


class CanWorkWithUserData(permissions.BasePermission):
    """
    Permissions for "User" model
    """

    def has_object_permission(self, request, view, obj):
        return True  # view.action in self._get_allowed_actions(request.user, obj)

    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)

    def _get_allowed_actions(self, user, obj=None):
        if not user.is_anonymous:
            if user.is_superuser:
                return self._get_superuser_allowed_actions(user, obj)
            else:
                return self._get_normal_user_allowed_actions(user, obj)
        else:
            return []

    def _get_superuser_allowed_actions(self, user, obj=None):
        if obj and obj.id == user.id:
            # Super user can do actions on his data:
            return ["list", "retrieve", "update", "partial_update", "destroy"]
        else:
            # Superadmin can list and retrive all objects, also create new users
            return ["create", "list", "retrieve"]

    def _get_normal_user_allowed_actions(self, user, obj=None):
        if obj and obj.id == user.id:
            # Normal user can do actions on his data:
            return ["list", "retrieve", "update", "partial_update", "destroy"]
        else:
            # Otherwise just listing users (only his record will be in the list):
            return ["list"]
