from rest_framework import serializers
from menuratings.menuratings.models import (
    Restaurant,
    RestaurantRepresenter,
    Menu,
    Organization,
    OrganizationRepresenter,
    Vote,
)


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["id", "name"]


class RestaurantRepresenterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RestaurantRepresenter
        fields = ["id", "user", "restaurant"]


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "date", "contents"]


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name"]


class OrganizationRepresenterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrganizationRepresenter
        fields = ["id", "user", "organization", "is_org_admin"]


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = ["id", "voter", "menu"]
