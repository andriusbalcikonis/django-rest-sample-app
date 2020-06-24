from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .mr.views import (
    MyUserViewSet,
    MyRestaurantTodaysMenuViewSet,
    MyTodaysOptionsViewSet,
    AdminRestaurantViewSet,
    AdminMenuViewSet,
    AdminOrganizationViewSet,
    AdminVoteViewSet,
    AdminUserViewSet,
)

router = DefaultRouter()
router.register(r"my-user", MyUserViewSet, basename="my-user")
router.register(
    r"my-restaurant-todays-menu",
    MyRestaurantTodaysMenuViewSet,
    basename="my-restaurant-todays-menu",
)
router.register(
    r"my-todays-options", MyTodaysOptionsViewSet, basename="my-restaurant-todays-menu",
)
router.register(r"admin-users", AdminUserViewSet)
router.register(r"admin-restaurants", AdminRestaurantViewSet)
router.register(r"admin-menus", AdminMenuViewSet)
router.register(r"admin-organizations", AdminOrganizationViewSet)
router.register(r"admin-votes", AdminVoteViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api-token-auth/", views.obtain_auth_token),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
