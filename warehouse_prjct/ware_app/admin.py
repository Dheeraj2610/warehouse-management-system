from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CustomerModel)
admin.site.register(Delivery)
admin.site.register(Notification)
admin.site.register(Product)
# admin.site.register(Order)
admin.site.register(CartModel)
admin.site.register(ShippingMethod)
