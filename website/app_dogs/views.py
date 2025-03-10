"""API endpoints in the app_dogs."""

from rest_framework import viewsets

from app_dogs.models import Breed, Dog
from app_dogs.serializers import (
    BreedSerializer,
    DogListSerializer,
    DogDetailSerializer,
)


class DogViewSet(viewsets.ModelViewSet):
    """DRF ViewSet for the Dog entity."""

    queryset = Dog.objects.all().order_by("id").select_related("breed")

    def get_serializer_class(self):
        """Return different serializers for list and detail actions."""
        if self.action == "list":
            return DogListSerializer

        return DogDetailSerializer


class BreedViewSet(viewsets.ModelViewSet):
    """DRF ViewSet for the Breed entity."""

    queryset = Breed.objects.all().order_by("id")
    serializer_class = BreedSerializer
