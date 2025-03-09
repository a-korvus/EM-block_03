"""Django models representing entities in the database."""

from django.db import models

from app_dogs.utils.choises import GenderChioce, RatingChoice, SizeChioce


class Dog(models.Model):
    """Dog entity in the database."""

    name = models.CharField(max_length=255, null=False)
    age = models.PositiveSmallIntegerField(null=False)
    breed = models.ForeignKey(
        to="Breed",
        on_delete=models.PROTECT,
        null=True,
        default=None,
        related_name="dogs",
    )
    gender = models.CharField(
        max_length=6,
        choices=GenderChioce,
        default=GenderChioce.MALE,
        help_text="Select a gender of the dog: male or female."
    )
    color = models.CharField(max_length=255, default="other")
    favorite_food = models.CharField(max_length=255, null=True, default=None)
    favorite_toy = models.CharField(max_length=255, null=True, default=None)

    def __str__(self) -> str:
        """Set up the string representation of the Model."""
        return f"<{self.id}> '{self.name}'"


class Breed(models.Model):
    """Breed entity in the database."""

    name = models.CharField(max_length=255, null=False)
    size = models.CharField(
        max_length=6,
        choices=SizeChioce,
        default=SizeChioce.MEDIUM,
    )
    friendliness = models.PositiveSmallIntegerField(
        choices=RatingChoice,
        default=RatingChoice.THREE,
    )
    trainability = models.PositiveSmallIntegerField(
        choices=RatingChoice,
        default=RatingChoice.THREE,
    )
    shedding_amount = models.PositiveSmallIntegerField(
        choices=RatingChoice,
        default=RatingChoice.THREE,
    )
    exercise_needs = models.PositiveSmallIntegerField(
        choices=RatingChoice,
        default=RatingChoice.THREE,
    )

    def __str__(self) -> str:
        """Set up the string representation of the Model."""
        return f"<{self.id}> '{self.name}'"
