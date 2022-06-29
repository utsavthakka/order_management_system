from rest_framework import status
import logging
from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from .models import Order, OrderQuantity, User, Product
from .serializers import ConsumerSerializer, OrderQuantitySerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.
logger = logging.getLogger(__name__)


class CreateConsumerViewset(viewsets.ModelViewSet):
    """
    # Sample Request payload
    {
        "username": "utsajv343",
        "email": "Utseadwv@gmail.com",
        "password": "Utsav@0988",
        "user_type": "consumer",
    }
    
    ## Sample Response Payload
    {
        "username": "utsajv343",
        "email": "Utseadwv@gmail.com",
        "user_type": "consumer",
    }
    """
    queryset = User.objects.all()
    serializer_class = ConsumerSerializer
    http_method_names = ["post"]


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = (TokenAuthentication,)
    serializer_class = OrderQuantitySerializer
    http_method_names = ["post"]
    queryset = Order.objects.all()

    """
    ## Sample Request Payload
    {"product": {"1": 3, "2": 4}}

    ## Sample Response Payload

       {
        "success": true,
        "message": "Order Added Successfully.",
        "payload": {
            "id": 28,
            "user": 3,
            "order": [
                {
                    "product": {
                        "id": 1,
                        "name": "shooes",
                        "description": "shoes",
                        "price": 12.9,
                        "created_at": "2022-06-27T16:41:30.989014Z",
                        "modified_at": "2022-06-27",
                        "is_active": true
                    },
                    "quantity": 3
                },
                {
                    "product": {
                        "id": 2,
                        "name": "Shirt",
                        "description": "Very Good Shirt",
                        "price": 10.0,
                        "created_at": "2022-06-28T05:42:36.654312Z",
                        "modified_at": "2022-06-28",
                        "is_active": true
                    },
                    "quantity": 4
                }
            ]
        }
    }
    """

    ## This view set is used to create the order with quentity

    def create(self, request):
        ## It will check the user type it is consumer or not
        if not request.user.user_type == "consumer":
            return Response(
                {"success": True, "message": "User is not consumer.", "payload": []}
            )

        serializer = OrderQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if len(serializer.validated_data["product"]) > 0:
            ## This is used to create the order with multiple product
            order_object = Order.objects.create(user=request.user)
            OrderQuantity.objects.bulk_create(
                [
                    OrderQuantity(
                        product=Product.objects.filter(id=int(key)).first(),
                        quantity=value,
                        order=order_object,
                    )
                    for key, value in serializer.validated_data["product"].items()
                    if Product.objects.filter(id=key).exists()
                ]
            )

            order_detail = Order.objects.filter(id=order_object.id).prefetch_related(
                Prefetch("order")
            )
            order = OrderSerializer(order_detail[0])
            return Response(
                {
                    "success": True,
                    "message": "Order Added Successfully.",
                    "payload": order.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "success": True,
                "message": "There is no product in request.",
                "payload": [],
            },
            status=status.HTTP_200_OK,
        )


class MyOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    """
    ## Sample Response Payload
        {
        "success": true,
        "message": "User Order Detail Fetch Successfully.",
        "payload": [
            {
                "id": 25,
                "user": 3,
                "order": [
                    {
                        "product": {
                            "id": 1,
                            "name": "shooes",
                            "description": "shoes",
                            "price": 12.9,
                            "created_at": "2022-06-27T16:41:30.989014Z",
                            "modified_at": "2022-06-27",
                            "is_active": true
                        },
                        "quantity": 3
                    }
                ]
            },
            {
                "id": 26,
                "user": 3,
                "order": [
                    {
                        "product": {
                            "id": 1,
                            "name": "shooes",
                            "description": "shoes",
                            "price": 12.9,
                            "created_at": "2022-06-27T16:41:30.989014Z",
                            "modified_at": "2022-06-27",
                            "is_active": true
                        },
                        "quantity": 3
                    }
                ]
            }
        ]
    }
    """
    ## This list is used To fetch all order of the user

    def list(self, request):
        order_detail = Order.objects.filter(user=request.user.id).prefetch_related(
            Prefetch("order")
        )
        order = OrderSerializer(order_detail, many=True)
        return Response(
            {
                "success": True,
                "message": "User Order Detail Fetch Successfully.",
                "payload": order.data,
            },
            status=status.HTTP_200_OK,
        )
