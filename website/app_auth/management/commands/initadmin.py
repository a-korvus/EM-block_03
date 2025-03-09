"""Management command to initialize superuser."""

import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth. models import User


class Command(BaseCommand):
    """Command realization."""

    help = "Create a superuser non-interactively if it doesn't exist."

    def handle(self, *args, **options):
        """Run it as management command."""
        user: User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin")

        if not user.objects.filter(username=username).exists():
            user.objects.create_superuser(username, email, password)
            self.stdout.write(
                self.style.SUCCESS(f"Superuser {username} created.")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Superuser {username} already exists.")
            )
