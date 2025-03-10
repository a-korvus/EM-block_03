"""Tests for the Dog Model API.

Check the following operations:
All data set:
    - GET: get all dogs;
    - POST: create a new one Dog entity.
A one of the dogs:
    - GET: get detail data of the Dog;
    - PUT: update detail data of the Dog;
    - DELETE: drop the Dog instance.
"""

import json

from django.db.models.query import QuerySet
from django.urls import reverse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from app_dogs.models import Breed, Dog


class DogAPITestCase(APITestCase):
    """Tests Dog API."""

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Set up data for the entire APITestCase.

        This method is executed once before any tests run.
        """
        base_url = "http://testserver"
        dog_detail_viewname = "app_dogs:dogs-detail"

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

        cls.url_dogs_base = reverse("app_dogs:dogs-list")

        cls.url_dog_detail_1 = base_url + reverse(
            dog_detail_viewname,
            args=(cls.dog_1.id,),
        )
        cls.url_dog_detail_2 = base_url + reverse(
            dog_detail_viewname,
            args=(cls.dog_2.id,),
        )
        cls.url_dog_detail_3 = base_url + reverse(
            dog_detail_viewname,
            args=(cls.dog_3.id,),
        )

    def test_get_all(self):
        """Check how you get list of the dogs."""
        expected_data = [
            {
                "id": self.dog_1.id,
                "name": "Axe",
                "age": 3,
                "gender": "male",
                "detail_url": self.url_dog_detail_1,
            },
            {
                "id": self.dog_2.id,
                "name": "Bryee",
                "age": 2,
                "gender": "female",
                "detail_url": self.url_dog_detail_2,
            },
            {
                "id": self.dog_3.id,
                "name": "Dutty",
                "age": 4,
                "gender": "female",
                "detail_url": self.url_dog_detail_3,
            },
        ]

        response: Response = self.client.get(self.url_dogs_base)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data["results"])

    def test_post_create(self):
        """Check how you can create a new Dog entity."""
        new_dog_data = {
            "name": "Lucia",
            "age": 3,
            "gender": "female",
        }
        dogs_before_post: int = Dog.objects.all().count()
        response_data = {
            "path": self.url_dogs_base,
            "data": json.dumps(new_dog_data),
            "content_type": "application/json",
        }

        response: Response = self.client.post(**response_data)

        dogs_after_post: int = Dog.objects.all().count()
        new_dog: Dog = Dog.objects.last()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(dogs_before_post + 1, dogs_after_post)
        self.assertEqual(new_dog_data["name"], new_dog.name)
        self.assertEqual("other", new_dog.color)

    def test_get_one(self):
        """Check how you get the dog by ID."""
        expected_data_1 = {
            "id": self.dog_1.id,
            "name": "Axe",
            "age": 3,
            "gender": "male",
            "color": "other",
            "favorite_food": None,
            "favorite_toy": None,
            "breed": self.breed_1.id,
        }
        expected_data_2 = {
            "id": self.dog_2.id,
            "name": "Bryee",
            "age": 2,
            "gender": "female",
            "color": "black",
            "favorite_food": "beef",
            "favorite_toy": "ball",
            "breed": self.breed_2.id,
        }
        expected_data_3 = {
            "id": self.dog_3.id,
            "name": "Dutty",
            "age": 4,
            "gender": "female",
            "color": "gray",
            "favorite_food": "pork",
            "favorite_toy": "bone",
            "breed": self.breed_2.id,
        }

        response_dog_1: Response = self.client.get(self.url_dog_detail_1)
        response_dog_2: Response = self.client.get(self.url_dog_detail_2)
        response_dog_3: Response = self.client.get(self.url_dog_detail_3)

        self.assertEqual(status.HTTP_200_OK, response_dog_1.status_code)
        self.assertEqual(status.HTTP_200_OK, response_dog_2.status_code)
        self.assertEqual(status.HTTP_200_OK, response_dog_3.status_code)

        self.assertEqual(expected_data_1, response_dog_1.data)
        self.assertEqual(expected_data_2, response_dog_2.data)
        self.assertEqual(expected_data_3, response_dog_3.data)

    def test_put_one(self):
        """Check how you can update the existing Dog instance."""
        updated_data = {
            "id": self.dog_2.id,
            "name": "Bryee",
            "age": 3,
            "color": "dark gray",
        }

        response_data = {
            "path": self.url_dog_detail_2,
            "data": json.dumps(updated_data),
            "content_type": "application/json",
        }

        dog_before_update: Dog = Dog.objects.get(id=self.dog_2.id)
        response: Response = self.client.put(**response_data)
        dog_after_update: Dog = Dog.objects.get(id=self.dog_2.id)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertNotEqual(dog_before_update.age, dog_after_update.age)
        self.assertNotEqual(dog_before_update.color, dog_after_update.color)

        self.assertEqual(updated_data["age"], dog_after_update.age)
        self.assertEqual(updated_data["color"], dog_after_update.color)

    def test_delete_one(self):
        """Check how you can drop the Dog instance."""
        dogs_before_deleting: QuerySet = Dog.objects.all().count()
        response: Response = self.client.delete(self.url_dog_detail_1)
        dogs_after_deleting: QuerySet = Dog.objects.all().count()

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(dogs_before_deleting - 1, dogs_after_deleting)
