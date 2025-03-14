"""Urls in this app 'app_dogs'."""

from app_dogs.views import BreedViewSet, DogViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"dogs", DogViewSet, basename="dogs")
router.register(r"breeds", BreedViewSet, basename="breeds")

app_name = "app_dogs"

urlpatterns = [
    path("", include(router.urls)),
]
