from rest_framework import permissions
from menuratings.mr.helpers.external_dependencies import get_todays_date
from menuratings.mr.models import Menu, Vote


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
        if (
            not request.user.is_anonymous
            and menu_item.restaurant_id == request.user.represented_restaurant_id
        ):
            return menu_item.date == get_todays_date()
        else:
            return False

    def has_permission(self, request, view):

        user_is_representing_any_restaurant = not request.user.is_anonymous and bool(
            request.user.represented_restaurant_id
        )

        if user_is_representing_any_restaurant:
            if view.action == "create":
                # Allow to upload only if nothing was uploaded today for this restaurant:
                num_of_already_posted_today_by_my_restaurant = (
                    Menu.objects.filter(
                        restaurant_id=request.user.represented_restaurant_id
                    )
                    .filter(date=get_todays_date())
                    .count()
                )
                can_upload_another_menu = (
                    num_of_already_posted_today_by_my_restaurant == 0
                )
                return can_upload_another_menu
            else:
                # If I represent any restaurant, actions are allowed
                # (detailed checks will be in has_object_permission)
                return True
        else:
            # If not restaurant representer, no actions allowed
            return False


class CanAccessMyVotes(permissions.BasePermission):
    """
    Permissions for my votes
    """

    def has_permission(self, request, view):
        if self.user_represents_any_org(request):
            if view.action == "create":
                # Allow to vote only if this is my first vote today
                num_of_my_votes_today = (
                    Vote.objects.filter(voter_id=request.user.id)
                    .filter(menu__date=get_todays_date())
                    .count()
                )
                can_post_another_vote = num_of_my_votes_today == 0
                return can_post_another_vote
            else:
                # If I represent any org, actions are allowed
                # (detailed checks will be in has_object_permission)
                return True
        else:
            # If not org representer, no actions allowed
            return False

    def has_object_permission(self, request, view, vote_item):
        return (
            self.user_represents_any_org(request)
            and vote_item.voter_id == request.user.id
        )

    def user_represents_any_org(self, request):
        return not request.user.is_anonymous and request.user.represented_organization
