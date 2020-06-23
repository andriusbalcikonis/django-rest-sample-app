from rest_framework import serializers
from menuratings.mr.models import (
    Restaurant,
    RestaurantRepresenter,
    Menu,
    Organization,
    OrganizationRepresenter,
    Vote,
    User,
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            "url",
            "id",
            "username",
            "first_name",
            "last_name",
        )
        read_only_fields = ("username",)


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


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["url", "id", "name"]


class RestaurantRepresenterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RestaurantRepresenter
        fields = ["url", "id", "user", "restaurant"]


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Menu
        fields = ["url", "id", "date", "contents"]


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ["url", "id", "name"]


class OrganizationRepresenterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrganizationRepresenter
        fields = ["url", "id", "user", "organization", "is_org_admin"]


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = ["url", "id", "voter", "menu"]
