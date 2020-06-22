import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Restaurant(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


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
