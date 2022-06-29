import imp
from itertools import product
from django.contrib import admin
from .models import Order, OrderQuantity, Product, User
# Register your models here.


ModelField= lambda model: type('Subclass'+model.__name__,(admin.ModelAdmin,),{
  'list_display':[x.name for x in model._meta.fields],
})

admin.site.register(User, ModelField(User))
admin.site.register(Order, ModelField(Order))
admin.site.register(OrderQuantity, ModelField(OrderQuantity))
admin.site.register(Product, ModelField(Product))
