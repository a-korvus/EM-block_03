"""Tests as serializers make transformations of model data in app_dogs."""

from django.test import RequestFactory, TestCase
from django.urls import reverse

from app_dogs.models import Breed, Dog
from app_dogs.serializers import (
    BreedSerializer,
    DogDetailSerializer,
    DogListSerializer,
)


class SerializersTestCase(TestCase):
    """Main check of all serializers."""

    def setUp(self):
        """Run this method before each test function in this class.

        Create some test data.
        """
        self.factory = RequestFactory()
        self.request = self.factory.get("")

        breed_detail_viewname = "app_dogs:breeds-detail"
        dog_detail_viewname = "app_dogs:dogs-detail"

        self.breed_1 = Breed.objects.create(
            name="pitbull",
            friendliness=5,
            trainability=5,
            shedding_amount=1,
        )
        self.breed_2 = Breed.objects.create(
            name="bandog",
            size="large",
            friendliness=2,
            shedding_amount=2,
            exercise_needs=5,
        )
        self.breed_3 = Breed.objects.create(
            name="bull terrier",
            size="small",
            friendliness=5,
            trainability=4,
            shedding_amount=2,
            exercise_needs=2,
        )

        self.dog_1: Dog = Dog.objects.create(
            name="Axe",
            age=3,
            breed=self.breed_1,
        )
        self.dog_2: Dog = Dog.objects.create(
            name="Bryee",
            age=2,
            gender="female",
            color="black",
            favorite_food="beef",
            favorite_toy="ball",
            breed=self.breed_2,
        )
        self.dog_3: Dog = Dog.objects.create(
            name="Dutty",
            age=4,
            gender="female",
            color="gray",
            favorite_food="pork",
            favorite_toy="bone",
            breed=self.breed_2,
        )

        self.url_breed_detail_1 = self.request.build_absolute_uri(
            reverse(breed_detail_viewname, args=(self.breed_1.id,))
        )
        self.url_breed_detail_2 = self.request.build_absolute_uri(
            reverse(breed_detail_viewname, args=(self.breed_2.id,))
        )
        self.url_breed_detail_3 = self.request.build_absolute_uri(
            reverse(breed_detail_viewname, args=(self.breed_3.id,))
        )

        self.url_dog_detail_1 = self.request.build_absolute_uri(
            reverse(dog_detail_viewname, args=(self.dog_1.id,))
        )
        self.url_dog_detail_2 = self.request.build_absolute_uri(
            reverse(dog_detail_viewname, args=(self.dog_2.id,))
        )
        self.url_dog_detail_3 = self.request.build_absolute_uri(
            reverse(dog_detail_viewname, args=(self.dog_3.id,))
        )

    def test_dog_list_serializer(self):
        """Test the operation of DogListSerializer."""
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
        serialized_data: dict = DogListSerializer(
            [self.dog_1, self.dog_2, self.dog_3],
            many=True,
            context={"request": self.request},
        ).data

        self.assertEqual(expected_data, serialized_data)

    def test_dog_detail_serializer(self):
        """Test the operation of DogDetailSerializer."""
        expected_data_dog_1 = {
            "id": self.dog_1.id,
            "name": "Axe",
            "age": 3,
            "gender": "male",
            "color": "other",
            "favorite_food": None,
            "favorite_toy": None,
            "breed": self.breed_1.id,
        }
        expected_data_dog_2 = {
            "id": self.dog_2.id,
            "name": "Bryee",
            "age": 2,
            "gender": "female",
            "color": "black",
            "favorite_food": "beef",
            "favorite_toy": "ball",
            "breed": self.breed_2.id,
        }
        expected_data_dog_3 = {
            "id": self.dog_3.id,
            "name": "Dutty",
            "age": 4,
            "gender": "female",
            "color": "gray",
            "favorite_food": "pork",
            "favorite_toy": "bone",
            "breed": self.breed_2.id,
        }

        serialized_data_dog_1: dict = DogDetailSerializer(self.dog_1).data
        serialized_data_dog_2: dict = DogDetailSerializer(self.dog_2).data
        serialized_data_dog_3: dict = DogDetailSerializer(self.dog_3).data

        self.assertEqual(expected_data_dog_1, serialized_data_dog_1)
        self.assertEqual(expected_data_dog_2, serialized_data_dog_2)
        self.assertEqual(expected_data_dog_3, serialized_data_dog_3)

    def test_breed_serializer(self):
        """Test the operation of BreedSerializer."""
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
            }
        ]
        serialized_data: dict = BreedSerializer(
            [self.breed_1, self.breed_2, self.breed_3],
            many=True,
            context={"request": self.request},
        ).data

        serialized_data_breed_1: dict = BreedSerializer(
            self.breed_1,
            context={"request": self.request},
        ).data
        serialized_data_breed_2: dict = BreedSerializer(
            self.breed_2,
            context={"request": self.request},
        ).data
        serialized_data_breed_3: dict = BreedSerializer(
            self.breed_3,
            context={"request": self.request},
        ).data

        self.assertEqual(expected_data, serialized_data)
        self.assertEqual(expected_data[0], serialized_data_breed_1)
        self.assertEqual(expected_data[1], serialized_data_breed_2)
        self.assertEqual(expected_data[2], serialized_data_breed_3)
