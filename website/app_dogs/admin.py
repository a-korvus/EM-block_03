"""Admin panel settings for the app_dogs."""

from app_dogs.models import Breed, Dog
from django.contrib import admin


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    """
    Dog Model representation in the admin panel of the site.

    Args:
        admin.ModelAdmin: Django model for the set up in the admin panel.
    """

    list_display = (
        "id",
        "name",
        "age",
        "gender",
    )
    list_display_links = (
        "id",
        "name",
    )
    ordering = ("id",)


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    """
    Breed Model representation in the admin panel of the site.

    Args:
        admin.ModelAdmin: Django model for the set up in the admin panel.
    """

    list_display = (
        "id",
        "name",
        "size",
    )
    list_display_links = (
        "id",
        "name",
    )
    ordering = ("id",)
