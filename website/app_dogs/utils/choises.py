"""Model fields with predefined choices."""

from django.db import models


class GenderChioce(models.TextChoices):
    """
    All available gender values.

    Args:
        models.TextChoices: Django model field.
    """

    MALE = (
        "male",
        "Male",
    )
    FEMALE = (
        "female",
        "Female",
    )


class SizeChioce(models.TextChoices):
    """All available size values.

    Args:
        models.TextChoices: Django model field.
    """

    TINY = (
        "tiny",
        "Tiny",
    )
    SMALL = (
        "small",
        "Small",
    )
    MEDIUM = (
        "medium",
        "Medium",
    )
    LARGE = (
        "large",
        "Large",
    )


class RatingChoice(models.IntegerChoices):
    """All available rating values.

    Args:
        models.TextChoices: Django model field.
    """

    ONE = (
        1,
        "1",
    )
    TWO = (
        2,
        "2",
    )
    THREE = (
        3,
        "3",
    )
    FOUR = (
        4,
        "4",
    )
    FIVE = (
        5,
        "5",
    )
