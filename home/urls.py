from rest_framework import routers, urlpatterns
from .views import CreateConsumerViewset, OrderViewSet, MyOrderViewSet
from django.urls import path,include

router = routers.DefaultRouter()
router.register('create_consumer', CreateConsumerViewset, 'consumer')
router.register('order',OrderViewSet,'order')
router.register("myorder", MyOrderViewSet, "myorder"),
# urlpatterns=router.urls
urlpatterns = [
    path("", include(router.urls)),
]


    