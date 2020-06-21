from django.db import models
from menuratings.users.models import User


class Restaurant(models.Model):
    name = models.TextField()


class RestaurantRepresenter(models.Model):
    user = models.ForeignKey(
        User, related_name="represented_restaurants", on_delete=models.CASCADE
    )
    restaurant = models.ForeignKey(
        Restaurant, related_name="users", on_delete=models.CASCADE
    )


class Menu(models.Model):
    date = models.DateField()
    contents = models.TextField()


class Organization(models.Model):
    name = models.TextField()


class OrganizationRepresenter(models.Model):
    user = models.ForeignKey(
        User, related_name="represented_organizations", on_delete=models.CASCADE
    )
    organization = models.ForeignKey(
        Organization, related_name="users", on_delete=models.CASCADE
    )
    is_org_admin = models.BooleanField()


class Vote(models.Model):
    voter = models.ForeignKey(
        OrganizationRepresenter, related_name="votes", on_delete=models.CASCADE
    )
    menu = models.ForeignKey(Menu, related_name="votes", on_delete=models.CASCADE)
