"""Admin panel settings for the app_dogs."""

from django.contrib import admin

from app_dogs.models import Breed, Dog


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    """Dog Model representation in the admin panel of the site."""

    list_display = "id", "name", "age", "gender",
    list_display_links = "id", "name",
    ordering = "id",


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    """Breed Model representation in the admin panel of the site."""

    list_display = "id", "name", "size",
    list_display_links = "id", "name",
    ordering = "id",
