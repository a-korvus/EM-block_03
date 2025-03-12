"""Configuration module of django application."""

from django.apps import AppConfig


class AppAuthConfig(AppConfig):
    """
    Django config for app_auth.

    Args:
        AppConfig: Django AppConfig.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app_auth"
