"""Serializers in the app_dogs."""

from rest_framework import serializers

from app_dogs.models import Breed, Dog


class DogListSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for listing Dogs with minimal fields."""

    detail_url = serializers.HyperlinkedIdentityField(
        view_name="app_dogs:dogs-detail",
        lookup_field="pk",
    )

    class Meta:
        model = Dog
        fields = "id", "name", "age", "gender", "detail_url",


class DogDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed Dog view with all fields."""

    class Meta:
        model = Dog
        fields = "__all__"


class BreedListSerializer(serializers.HyperlinkedModelSerializer):
    """Specify how you want to serialize Breed entities."""

    detail_url = serializers.HyperlinkedIdentityField(
        view_name="app_dogs:breeds-detail",
        lookup_field="pk",
    )

    class Meta:
        model = Breed
        fields = [field.name for field in Breed._meta.fields] + ["detail_url"]


class BreedDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed Breed view with all fields."""

    class Meta:
        model = Breed
        fields = "__all__"
