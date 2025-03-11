"""Serializers in the app_dogs."""

from app_dogs.models import Breed, Dog
from rest_framework import serializers


class DogListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for listing Dogs with minimal fields.

    Args:
        HyperlinkedModelSerializer: DRF serializer based on django model.
        Processed detail links.
    """

    breed_avg_age = serializers.FloatField(read_only=True)
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="app_dogs:dogs-detail",
        lookup_field="pk",
    )

    class Meta:
        """
        Serializer django Meta class.

        Define a related model and serializable fields.
        """

        model = Dog
        fields = (
            "id",
            "name",
            "age",
            "gender",
            "detail_url",
            "breed_avg_age",
        )


class DogDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed Dog view with all fields.

    Args:
        ModelSerializer: DRF serializer based on django model.
    """

    same_breed_count = serializers.IntegerField(read_only=True)

    class Meta:
        """
        Serializer django Meta class.

        Define a related model and serializable fields.
        """

        model = Dog
        fields = (
            "id",
            "name",
            "age",
            "gender",
            "breed",
            "color",
            "favorite_food",
            "favorite_toy",
            "same_breed_count",
        )


class BreedListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Specify how you want to serialize Breed entities.

    Args:
        HyperlinkedModelSerializer: DRF serializer based on django model.
        Processed detail links.
    """

    dog_count = serializers.IntegerField(read_only=True)
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="app_dogs:breeds-detail",
        lookup_field="pk",
    )

    class Meta:
        """
        Serializer django Meta class.

        Define a related model and serializable fields.
        """

        model = Breed
        fields = [field.name for field in Breed._meta.fields] + [
            "detail_url",
            "dog_count",
        ]


class BreedDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed Breed view with all fields.

    Args:
        ModelSerializer: DRF serializer based on django model.
    """

    class Meta:
        """
        Serializer django Meta class.

        Define a related model and serializable fields.
        """

        model = Breed
        fields = "__all__"
