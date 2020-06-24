from rest_framework import viewsets
from .permissions import CanWorkWithMyUserData, CanWorkWithAnyUserData, IsSuperAdmin
from menuratings.mr.models import Restaurant, Menu, Organization, User, Vote
from menuratings.mr.serializers import (
    RestaurantSerializer,
    MenuSerializer,
    OrganizationSerializer,
    VoteSerializer,
    UserSerializer,
    UserSerializerForAdmin,
    CreateUserSerializer,
)


class MyUserViewSet(viewsets.ModelViewSet):

    permission_classes = (CanWorkWithMyUserData,)

    def get_queryset(self):
        """
        Filter objects so a user only sees his own stuff.
        If user is admin, let him see all.
        """
        if self.request.user.is_anonymous:
            return User.objects.none()
        else:
            return User.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == "list":
            return UserSerializer
        elif self.action == "create":
            return CreateUserSerializer
        else:
            return UserSerializer


class AdminUserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializerForAdmin
    permission_classes = [CanWorkWithAnyUserData]


class AdminRestaurantViewSet(viewsets.ModelViewSet):

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsSuperAdmin]


class AdminMenuViewSet(viewsets.ModelViewSet):

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsSuperAdmin]


class AdminOrganizationViewSet(viewsets.ModelViewSet):

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsSuperAdmin]


class AdminVoteViewSet(viewsets.ModelViewSet):

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsSuperAdmin]
