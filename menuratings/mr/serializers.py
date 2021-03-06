from rest_framework import serializers
from menuratings.mr.models import (
    Restaurant,
    Menu,
    Organization,
    Vote,
    User,
)
from menuratings.mr.helpers.external_dependencies import get_todays_date
from menuratings.mr.helpers.complex_queries import get_voting_results_of_the_day


class CreateUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "auth_token",
        )
        read_only_fields = ("auth_token",)
        extra_kwargs = {"password": {"write_only": True}}


class UserSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name="my-user-detail")

    represented_restaurant = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )

    represented_organization = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )

    class Meta:
        model = User
        fields = (
            "url",
            "id",
            "username",
            "first_name",
            "last_name",
            "represented_restaurant",
            "represented_organization",
        )
        read_only_fields = (
            "username",
            "represented_restaurant",
            "represented_organization",
        )


class UserSerializerForAdmin(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            "url",
            "id",
            "username",
            "first_name",
            "last_name",
            "represented_restaurant",
            "represented_organization",
        )
        read_only_fields = ("username",)


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["url", "id", "name"]


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Menu
        fields = ["url", "id", "date", "contents", "restaurant", "file"]


class MyRestaurantTodaysMenuSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="my-restaurant-todays-menu-detail"
    )

    class Meta:
        model = Menu
        fields = ["url", "contents", "file"]


class MyTodaysOptionsMenuSerializer(serializers.HyperlinkedModelSerializer):

    restaurant = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )

    votes_in_my_organization = serializers.SerializerMethodField(
        "get_votes_in_my_organization"
    )

    def get_votes_in_my_organization(self, current_menu_item):
        """
        Calculates todays votes for this menu option and only in the context of users org.
        """

        current_user = self.get_context_user()

        if current_user:
            votes = (
                Vote.objects.filter(menu_id=current_menu_item.id)
                .filter(
                    voter__represented_organization_id=current_user.represented_organization.id
                )
                .count()
            )

            return votes
        else:
            return -1

    is_todays_winner = serializers.SerializerMethodField("get_is_todays_winner")

    def get_is_todays_winner(self, current_menu_item):
        stats = self.get_and_cache_stats()
        for line in stats:
            if (
                line.get("winner")
                and line.get("menu__restaurant_id") == current_menu_item.restaurant_id
            ):
                return True
        return False

    def get_and_cache_stats(self):

        request = self.context.get("request")
        cached_stats = request.mr_stats if hasattr(request, "mr_stats") else None

        if not cached_stats:
            today = get_todays_date()
            user = self.get_context_user()
            cached_stats = get_voting_results_of_the_day(
                today, user.represented_organization_id
            )
            request.mr_stats = cached_stats

        return cached_stats

    def get_context_user(self):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return request.user
        else:
            return None

    class Meta:
        model = Menu
        fields = [
            "restaurant",
            "contents",
            "file",
            "votes_in_my_organization",
            "is_todays_winner",
        ]


class MyVoteSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name="my-vote-detail")

    menu = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")

    class Meta:
        model = Vote
        fields = ["url", "id", "menu"]


class MyVoteSerializerForEditing(serializers.HyperlinkedModelSerializer):
    class MenuOptionsField(serializers.PrimaryKeyRelatedField):
        def get_queryset(self):
            today = get_todays_date()
            return Menu.objects.filter(date=today)

    menu = MenuOptionsField(many=False, read_only=False)

    class Meta:
        model = Vote
        fields = ["url", "id", "menu"]


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ["url", "id", "name"]


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = ["url", "id", "voter", "menu"]
