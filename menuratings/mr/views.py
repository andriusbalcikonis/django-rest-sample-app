from rest_framework import viewsets
from .permissions import (
    CanWorkWithMyUserData,
    CanWorkWithAnyUserData,
    IsSuperAdmin,
    IsOrganizationUser,
    CanWorkWithMyRestaurantMenu,
)
from menuratings.mr.models import Restaurant, Menu, Organization, User, Vote
from menuratings.mr.serializers import (
    RestaurantSerializer,
    MenuSerializer,
    MyRestaurantTodaysMenuSerializer,
    MyTodaysOptionsMenuSerializer,
    MyVoteSerializer,
    OrganizationSerializer,
    VoteSerializer,
    UserSerializer,
    UserSerializerForAdmin,
    CreateUserSerializer,
)
from menuratings.mr.external import get_todays_date


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


class MyRestaurantTodaysMenuViewSet(viewsets.ModelViewSet):

    serializer_class = MyRestaurantTodaysMenuSerializer
    permission_classes = [CanWorkWithMyRestaurantMenu]

    def get_queryset(self):
        """
        Filter menus only from my restaurant and from today
        """
        represented_restaurant_id = self.request.user.represented_restaurant_id
        today = get_todays_date()
        if represented_restaurant_id:
            return Menu.objects.filter(date=today).filter(
                restaurant_id=represented_restaurant_id
            )
        else:
            return Menu.objects.none()

    def perform_create(self, serializer):
        serializer.save(
            date=get_todays_date(), restaurant=self.request.user.represented_restaurant,
        )


class MyTodaysOptionsViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = MyTodaysOptionsMenuSerializer
    permission_classes = [IsOrganizationUser]

    def get_queryset(self):
        """
        Filter menus - what are options for today
        """
        today = get_todays_date()
        return Menu.objects.filter(date=today)


class MyVotesViewSet(viewsets.ModelViewSet):

    serializer_class = MyVoteSerializer
    permission_classes = [IsOrganizationUser]

    def get_queryset(self):
        """
        Filter all previous votes of this user
        """
        return Vote.objects.filter(voter_id=self.request.user.id)


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
