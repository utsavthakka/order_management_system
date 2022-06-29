import email
from urllib import request
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from  home.models import Order, User
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from django.test import TestCase

class TestUser(TestCase):

    def test_crate_user(self):
        User.objects.create(username="utsav",password="django",email="Utsav@gmil.com",user_type="consumer")


