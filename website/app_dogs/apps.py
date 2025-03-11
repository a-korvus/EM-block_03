"""Configuration module of django application."""

from django.apps import AppConfig


class AppDogsConfig(AppConfig):
    """
    Django config for app_dogs.

    Args:
        AppConfig: Django AppConfig.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app_dogs"
