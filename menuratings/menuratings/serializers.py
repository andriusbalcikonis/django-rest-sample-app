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
