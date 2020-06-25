import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from simple_history.models import HistoricalRecords


class Restaurant(models.Model):
    name = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Menu(models.Model):
    date = models.DateField()
    contents = models.TextField()
    file = models.FileField(blank=True, null=True, upload_to="menu_file_uplods")
    restaurant = models.ForeignKey(
        Restaurant, related_name="posted_menus", on_delete=models.CASCADE
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    @property
    def name(self):
        return "Restaurant '{}' menu of {}".format(self.restaurant, self.date)

    class Meta:
        unique_together = ["date", "restaurant"]


class Organization(models.Model):
    name = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    represented_restaurant = models.ForeignKey(
        Restaurant,
        related_name="users",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    represented_organization = models.ForeignKey(
        Organization,
        related_name="employees",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Vote(models.Model):
    voter = models.ForeignKey(User, related_name="votes", on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, related_name="votes", on_delete=models.CASCADE)
    history = HistoricalRecords()
