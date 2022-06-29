from enum import unique
from itertools import product
from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
# Create your models here.


class User(AbstractUser):
    USER_CHOICES = (
        ("consumer", "Consumer"),
        ("admin", "Admin"),
    )
    user_type = models.CharField(
        max_length=20, choices=USER_CHOICES, default="consumer"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("email",)

    def __str__(self):
        return str(self.username)
        
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class Order(models.Model):
    # products = models.ManyToManyField(Product, related_name="products")
    user = models.ForeignKey(
        User,
        related_name="user",
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": "consumer"},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.id) + " " + str(self.user)


class OrderQuantity(models.Model):
    order = models.ForeignKey(Order, related_name="order", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="product", on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.order) + " " + str(self.product)
