from rest_framework import serializers
from .models import Order, OrderQuantity, Product, User

## Serializer to create user as consumer
class ConsumerSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "password", "email", "user_type"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


## to take multiple product in form of dictionary


class OrderQuantitySerializer(serializers.Serializer):
    product = serializers.DictField()


## This serializer is used to display a Product detail in Response payload


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


## This serialiser is used to featch the quantity of the product
class OrderQuantityFetchSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderQuantity
        fields = ["product", "quantity"]


## This serializer is used to display the all order of the perticular user


class OrderSerializer(serializers.ModelSerializer):
    order = OrderQuantityFetchSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "user", "order"]
