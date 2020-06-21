from rest_framework import permissions


class CanWorkWithUserData(permissions.BasePermission):
    """
    Permissions for "User" model
    """

    def has_object_permission(self, request, view, obj):
        if not view.action:
            # Empty action is for "OPTIONS" request:
            return True
        else:
            return view.action in self._get_allowed_actions(request.user, obj)

    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)

    def _get_allowed_actions(self, user, obj=None):
        if user.is_anonymous:
            # Anonymous users can register
            return ["list", "create"]
        else:
            if user.is_superuser:
                # Superadmin user can do all actions on any user data:
                return ["list", "retrieve", "update", "destroy"]
            else:
                # Normal user can do actions on his data, but nothing else:
                other_user_data = obj and obj.id != user.id
                return (
                    [] if other_user_data else ["list", "retrieve", "update", "destroy"]
                )
