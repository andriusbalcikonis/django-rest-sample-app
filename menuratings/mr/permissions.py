from rest_framework import permissions
from menuratings.mr.external import get_todays_date


class IsSuperAdmin(permissions.BasePermission):
    """
    Allow actions only for admin
    """

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsOrganizationUser(permissions.BasePermission):
    """
    Allow actions only for organization users
    """

    def has_permission(self, request, view):
        return not request.user.is_anonymous and request.user.represented_organization


class CanWorkWithMyUserData(permissions.BasePermission):
    """
    Permissions for my user data
    """

    def has_object_permission(self, request, view, obj):
        return view.action in self._get_allowed_actions(request.user, obj)

    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)

    def _get_allowed_actions(self, user, obj=None):
        if user.is_anonymous:
            # Anonymous users can register
            return ["list", "create"]
        else:
            # Normal user can do actions on his data, but nothing else:
            other_user_data = obj and obj.id != user.id
            return [] if other_user_data else ["list", "retrieve", "update", "destroy"]


class CanWorkWithAnyUserData(permissions.BasePermission):
    """
    Permissions for users list for admin
    """

    def has_object_permission(self, request, view, obj):
        return view.action in self._get_allowed_actions(request.user, obj)

    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)

    def _get_allowed_actions(self, user, obj=None):
        if user.is_superuser:
            # Superusers can do everything, except create new (only anonymous users can do that)
            return ["list", "retrieve", "update", "destroy"]
        else:
            return []


class CanWorkWithMyRestaurantMenu(permissions.BasePermission):
    """
    Permissions for my restaurant menu
    """

    def has_object_permission(self, request, view, menu_item):
        if menu_item.restaurant_id == request.user.represented_restaurant_id:
            return menu_item.date == get_todays_date()
        else:
            return False

    def has_permission(self, request, view):
        user_is_representing_any_restaurant = bool(
            request.user.represented_restaurant_id
        )
        return user_is_representing_any_restaurant
