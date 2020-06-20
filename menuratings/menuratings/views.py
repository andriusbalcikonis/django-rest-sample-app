from menuratings.menuratings.models import (
    Restaurant,
    RestaurantRepresenter,
    Menu,
    Organization,
    OrganizationRepresenter,
    Vote
)
from menuratings.menuratings.serializers import (
    RestaurantSerializer,
    RestaurantRepresenterSerializer,
    MenuSerializer,
    OrganizationSerializer,
    OrganizationRepresenterSerializer,
    VoteSerializer
)
from rest_framework import viewsets


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class RestaurantRepresenterViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = RestaurantRepresenter.objects.all()
    serializer_class = RestaurantRepresenterSerializer


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


class OrganizationRepresenterViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = OrganizationRepresenter.objects.all()
    serializer_class = OrganizationRepresenterSerializer


class VoteViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer