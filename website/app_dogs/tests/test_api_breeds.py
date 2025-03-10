"""Tests for the Breed Model API.

Check the following operations:
All data set:
    - GET: get all breeds;
    - POST: create a new one Breed entity.
A one of the breeds:
    - GET: get detail data of the Breed;
    - PUT: update detail data of the Breed;
    - DELETE: drop the Breed instance.
"""

import json

from django.db.models.query import QuerySet
from django.urls import reverse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from app_dogs.models import Breed, Dog


class BreedAPITestCase(APITestCase):
    """Tests Breed API."""

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Set up data for the entire APITestCase.

        This method is executed once before any tests run.
        """
        base_url = "http://testserver"
        breed_detail_viewname = "app_dogs:breeds-detail"

        cls.breed_1 = Breed.objects.create(
            name="pitbull",
            friendliness=5,
            trainability=5,
            shedding_amount=1,
        )
        cls.breed_2 = Breed.objects.create(
            name="bandog",
            size="large",
            friendliness=2,
            shedding_amount=2,
            exercise_needs=5,
        )
        cls.breed_3 = Breed.objects.create(
            name="bull terrier",
            size="small",
            friendliness=5,
            trainability=4,
            shedding_amount=2,
            exercise_needs=2,
        )

        cls.dog_1: Dog = Dog.objects.create(
            name="Axe",
            age=3,
            breed=cls.breed_1,
        )
        cls.dog_2: Dog = Dog.objects.create(
            name="Bryee",
            age=2,
            gender="female",
            color="black",
            favorite_food="beef",
            favorite_toy="ball",
            breed=cls.breed_2,
        )
        cls.dog_3: Dog = Dog.objects.create(
            name="Dutty",
            age=4,
            gender="female",
            color="gray",
            favorite_food="pork",
            favorite_toy="bone",
            breed=cls.breed_2,
        )

        cls.url_breeds_base = reverse("app_dogs:breeds-list")

        cls.url_breed_detail_1 = base_url + reverse(
            breed_detail_viewname,
            args=(cls.breed_1.id,),
        )
        cls.url_breed_detail_2 = base_url + reverse(
            breed_detail_viewname,
            args=(cls.breed_2.id,),
        )
        cls.url_breed_detail_3 = base_url + reverse(
            breed_detail_viewname,
            args=(cls.breed_3.id,),
        )

    def test_get_all(self):
        """Check how you get list of the breeds."""
        expected_data = [
            {
                "id": self.breed_1.id,
                "name": "pitbull",
                "size": "medium",
                "friendliness": 5,
                "trainability": 5,
                "shedding_amount": 1,
                "exercise_needs": 3,
                "detail_url": self.url_breed_detail_1,
                "dog_count": 1,
            },
            {
                "id": self.breed_2.id,
                "name": "bandog",
                "size": "large",
                "friendliness": 2,
                "trainability": 3,
                "shedding_amount": 2,
                "exercise_needs": 5,
                "detail_url": self.url_breed_detail_2,
                "dog_count": 2,
            },
            {
                "id": self.breed_3.id,
                "name": "bull terrier",
                "size": "small",
                "friendliness": 5,
                "trainability": 4,
                "shedding_amount": 2,
                "exercise_needs": 2,
                "detail_url": self.url_breed_detail_3,
                "dog_count": 0,
            },
        ]

        response: Response = self.client.get(self.url_breeds_base)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data["results"])

    def test_post_create(self):
        """Check how you can create a new Breed entity."""
        new_breed_data = {
            "name": "dobermann",
            "size": "large",
            "friendliness": 4,
            "trainability": 2,
            "shedding_amount": 4,
        }
        breeds_before_post: int = Breed.objects.all().count()
        response_data = {
            "path": self.url_breeds_base,
            "data": json.dumps(new_breed_data),
            "content_type": "application/json",
        }

        response: Response = self.client.post(**response_data)

        breeds_after_post: int = Breed.objects.all().count()
        new_breed: Breed = Breed.objects.last()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(breeds_before_post + 1, breeds_after_post)
        self.assertEqual(new_breed_data["name"], new_breed.name)
        self.assertEqual(3, new_breed.exercise_needs)

    def test_get_one(self):
        """Check how you get the breed by ID."""
        expected_data_1 = {
            "id": self.breed_1.id,
            "name": "pitbull",
            "size": "medium",
            "friendliness": 5,
            "trainability": 5,
            "shedding_amount": 1,
            "exercise_needs": 3,
        }
        expected_data_2 = {
            "id": self.breed_2.id,
            "name": "bandog",
            "size": "large",
            "friendliness": 2,
            "trainability": 3,
            "shedding_amount": 2,
            "exercise_needs": 5,
        }
        expected_data_3 = {
            "id": self.breed_3.id,
            "name": "bull terrier",
            "size": "small",
            "friendliness": 5,
            "trainability": 4,
            "shedding_amount": 2,
            "exercise_needs": 2,
        }

        response_breed_1: Response = self.client.get(self.url_breed_detail_1)
        response_breed_2: Response = self.client.get(self.url_breed_detail_2)
        response_breed_3: Response = self.client.get(self.url_breed_detail_3)

        self.assertEqual(status.HTTP_200_OK, response_breed_1.status_code)
        self.assertEqual(status.HTTP_200_OK, response_breed_2.status_code)
        self.assertEqual(status.HTTP_200_OK, response_breed_3.status_code)

        self.assertEqual(expected_data_1, response_breed_1.data)
        self.assertEqual(expected_data_2, response_breed_2.data)
        self.assertEqual(expected_data_3, response_breed_3.data)

    def test_put_one(self):
        """Check how you can update the existing Breed instance."""
        updated_data = {
            "id": self.breed_2.id,
            "name": "bulldog",
            "friendliness": 3,
            "shedding_amount": 3,
        }

        response_data = {
            "path": self.url_breed_detail_2,
            "data": json.dumps(updated_data),
            "content_type": "application/json",
        }

        breed_before_update: Breed = Breed.objects.get(id=self.breed_2.id)
        response: Response = self.client.put(**response_data)
        breed_after_update: Breed = Breed.objects.get(id=self.breed_2.id)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertNotEqual(breed_before_update.name, breed_after_update.name)
        self.assertNotEqual(
            breed_before_update.friendliness,
            breed_after_update.friendliness,
        )
        self.assertNotEqual(
            breed_before_update.shedding_amount,
            breed_after_update.shedding_amount,
        )

        self.assertEqual(updated_data["name"], breed_after_update.name)
        self.assertEqual(
            updated_data["friendliness"],
            breed_after_update.friendliness,
        )
        self.assertEqual(
            updated_data["shedding_amount"],
            breed_after_update.shedding_amount,
        )

    def test_delete_one(self):
        """Check how you can drop the Breed instance."""
        breeds_before_deleting: QuerySet = Breed.objects.all().count()
        response: Response = self.client.delete(self.url_breed_detail_3)
        breeds_after_deleting: QuerySet = Breed.objects.all().count()

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(breeds_before_deleting - 1, breeds_after_deleting)
