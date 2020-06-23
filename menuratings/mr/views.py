from rest_framework import viewsets
from .permissions import CanWorkWithUserData, IsSuperAdmin
from menuratings.mr.models import Restaurant, Menu, Organization, User, Vote
from menuratings.mr.serializers import (
    RestaurantSerializer,
    MenuSerializer,
    OrganizationSerializer,
    VoteSerializer,
    UserSerializer,
    CreateUserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    permission_classes = (CanWorkWithUserData,)

    def get_queryset(self):
        """
        Filter objects so a user only sees his own stuff.
        If user is admin, let him see all.
        """
        if self.request.user.is_anonymous:
            return User.objects.none()
        elif self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == "list":
            return UserSerializer
        if self.action == "create":
            return CreateUserSerializer
        return UserSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsSuperAdmin]

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class MenuViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class VoteViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
