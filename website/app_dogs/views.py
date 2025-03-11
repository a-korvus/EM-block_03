"""API endpoints in the app_dogs."""

from app_dogs.models import Breed, Dog
from app_dogs.serializers import (
    BreedDetailSerializer,
    BreedListSerializer,
    DogDetailSerializer,
    DogListSerializer,
)
from django.db.models import (
    Avg,
    Count,
    FloatField,
    IntegerField,
    OuterRef,
    Subquery,
)
from django.db.models.query import QuerySet
from rest_framework import viewsets
from rest_framework.serializers import ModelSerializer


class DogViewSet(viewsets.ModelViewSet):
    """
    DRF ViewSet for the Dog entity.

    Args:
        viewsets.ModelViewSet: DRF view set including processing of
            standard HTTP methods.
    """

    queryset = Dog.objects.all().order_by("id").select_related("breed")

    def get_queryset(self) -> QuerySet[Dog]:
        """
        Return different querysets for list and detail actions.

        For list action, annotate each Dog with the average age
        of dogs of the same breed.
        For retrieve action, annotate each Dog with the count
        of dogs of the same breed.

        Returns:
            QuerySet[Dog]: Django QuerySet of Dog models after filtering
                and other custom actions.
        """
        qs = self.queryset

        if self.action == "list":
            avg_age_subquery = (
                Dog.objects.filter(breed=OuterRef("breed_id"))
                .values("breed")  # только значения поля breed
                .annotate(avg_age=Avg("age"))  # av age для каждой группы breed
                .values("avg_age")[:1]  # получить QuerySet
            )
            qs = qs.annotate(
                breed_avg_age=Subquery(
                    avg_age_subquery,
                    output_field=FloatField(),
                )
            )
        elif self.action == "retrieve":
            count_subquery = (
                Dog.objects.filter(breed=OuterRef("breed_id"))
                .values("breed")
                .annotate(breed_count=Count("id"))
                .values("breed_count")[:1]
            )
            qs = qs.annotate(
                same_breed_count=Subquery(
                    count_subquery,
                    output_field=IntegerField(),
                )
            )

        return qs

    def get_serializer_class(self) -> ModelSerializer:
        """
        Return different serializers for list and detail actions.

        Returns:
            ModelSerializer: DRF serializer based on django model.
        """
        if self.action == "list":
            return DogListSerializer
        return DogDetailSerializer


class BreedViewSet(viewsets.ModelViewSet):
    """
    DRF ViewSet for the Breed entity.

    Args:
        viewsets.ModelViewSet: DRF view set including processing of
            standard HTTP methods.
    """

    queryset = Breed.objects.all().prefetch_related("dogs").order_by("id")
    serializer_class = BreedListSerializer

    def get_queryset(self) -> QuerySet[Breed]:
        """
        Return different querysets for list and detail actions.

        Expend the queryset with annotated fields if you have requested
        a list of objects from db.

        Returns:
            QuerySet[Breed]: Django QuerySet of Breed models after filtering
                and other custom actions.
        """
        if self.action == "list":
            return (
                Breed.objects.all()
                .annotate(
                    dog_count=Count("dogs"),
                )
                .prefetch_related("dogs")
                .order_by("id")
            )
        return self.queryset

    def get_serializer_class(self) -> ModelSerializer:
        """
        Return different serializers for list and detail actions.

        Returns:
            ModelSerializer: DRF serializer based on django model.
        """
        if self.action == "list":
            return BreedListSerializer
        return BreedDetailSerializer
