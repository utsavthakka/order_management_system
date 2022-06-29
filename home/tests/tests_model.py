import email
from urllib import request
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from home.models import Order, User, Product, OrderQuantity
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APIClient
from django.test import TestCase


class TestUser(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="test", password="test",
                                        email="test@gmil.com", user_type="consumer")

        self.token = Token.objects.get(user=self.user.id)
# Test case for user model
    def test_create_user(self):
        User.objects.create(username="utsav", password="django",
                            email="Utsav@gmil.com", user_type="consumer")
# Test case for Product
    def test_create_product(self):
        Product.objects.create(
            name="shoes", description="very good", price=12.90)

# Test  create consumer api
    def test_create_consumer(self):
        response = self.client.post(
            reverse("consumer-list"),
            {
                "username": "testuser",
                "password": "testpass",
                "email": "test@gmail.com"
            },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
# Test Create Order Api
    def test_create_orders(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.post(reverse("order-list"),
                               {
            "product": {
                "1": 3,
                "2": 4
            }

        },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
# Test get order Api
    def test_get_myorders(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.get(reverse("myorder-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
