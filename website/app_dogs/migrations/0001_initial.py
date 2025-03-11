"""Initial migration."""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Django migration class. Define a Breed and a Dog models.

    Args:
        migrations.Migration: Django base migration class.
    """

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Breed",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "size",
                    models.CharField(
                        choices=[
                            ("tiny", "Tiny"),
                            ("small", "Small"),
                            ("medium", "Medium"),
                            ("large", "Large"),
                        ],
                        default="medium",
                        max_length=6,
                    ),
                ),
                (
                    "friendliness",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "1"),
                            (2, "2"),
                            (3, "3"),
                            (4, "4"),
                            (5, "5"),
                        ],
                        default=3,
                    ),
                ),
                (
                    "trainability",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "1"),
                            (2, "2"),
                            (3, "3"),
                            (4, "4"),
                            (5, "5"),
                        ],
                        default=3,
                    ),
                ),
                (
                    "shedding_amount",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "1"),
                            (2, "2"),
                            (3, "3"),
                            (4, "4"),
                            (5, "5"),
                        ],
                        default=3,
                    ),
                ),
                (
                    "exercise_needs",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "1"),
                            (2, "2"),
                            (3, "3"),
                            (4, "4"),
                            (5, "5"),
                        ],
                        default=3,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Dog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("age", models.PositiveSmallIntegerField()),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "Male"), ("female", "Female")],
                        default="male",
                        help_text="Select a gender of the dog: male or female.",  # noqa
                        max_length=6,
                    ),
                ),
                ("color", models.CharField(default="other", max_length=255)),
                (
                    "favorite_food",
                    models.CharField(default=None, max_length=255, null=True),
                ),
                (
                    "favorite_toy",
                    models.CharField(default=None, max_length=255, null=True),
                ),
                (
                    "breed",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="dogs",
                        to="app_dogs.breed",
                    ),
                ),
            ],
        ),
    ]
