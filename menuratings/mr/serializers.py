from rest_framework import serializers
from menuratings.mr.models import (
    Restaurant,
    Menu,
    Organization,
    Vote,
    User,
)


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
        fields = ["url", "id", "date", "contents", "restaurant"]


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ["url", "id", "name"]


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = ["url", "id", "voter", "menu"]
