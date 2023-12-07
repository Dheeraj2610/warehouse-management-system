from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CustomerModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    cs_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    cs_email = models.EmailField()
    cs_address = models.CharField(max_length=200)
    cs_gender = models.CharField(max_length=100)
    cs_pan = models.CharField(max_length=100)
    cs_phone = models.IntegerField()
    cs_image = models.ImageField(upload_to="image/", null=True)
    password = models.CharField(max_length=50)
    status = models.BooleanField(default=False)


class Delivery(models.Model):
    dl_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    dl_email = models.EmailField()
    password = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    dl_phone = models.IntegerField(null=True)
    dl_image = models.ImageField(upload_to="image/", null=True)


class Notification(models.Model):
    customer = models.ForeignKey(
        CustomerModel, on_delete=models.CASCADE, null=True, blank=True)
    delivery = models.ForeignKey(
        Delivery, on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_for = models.CharField(max_length=50, default='admin')


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    specifications = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    initial_stock_quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to="image/", null=True)
    customer = models.ForeignKey(
        CustomerModel, on_delete=models.CASCADE, null=True, blank=True)


class CartModel(models.Model):
    customer = models.ForeignKey(
        'CustomerModel', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)


class ShippingMethod(models.Model):
    name = models.CharField(max_length=50)


class Order(models.Model):
    PENDING = 'Pending'
    DISPATCHED = 'Dispatched'
    IN_TRANSIT = 'In Transit'
    DELIVERED = 'Delivered'

    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (DISPATCHED, 'Dispatched'),
        (IN_TRANSIT, 'In Transit'),
        (DELIVERED, 'Delivered'),
    ]

    customer = models.ForeignKey(
        'CustomerModel', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField()
    date_ordered = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES, default=PENDING)
    shipping_method = models.ForeignKey(
        ShippingMethod, on_delete=models.CASCADE, null=True)
    tracking_id = models.CharField(max_length=8, null=True)
    # extra added
    location = models.CharField(max_length=100, null=True)
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    delivery_person = models.ForeignKey(
        Delivery, on_delete=models.SET_NULL, null=True)
    location_dispatch = models.CharField(max_length=100, null=True)
    location_transit = models.CharField(max_length=100, null=True)
    admin_combined_status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES, default=PENDING)
    client_delivery_status = models.BooleanField(default=False)

    def update_admin_combined_status(self):
        if self.order_status == self.DELIVERED and self.client_delivery_status:
            self.admin_combined_status = self.DELIVERED
            self.save()


# class DeliveryStatus(models.Model):
#     DELIVERY_PENDING = 'Pending'
#     DELIVERY_DISPATCHED = 'Dispatched'
#     DELIVERY_IN_TRANSIT = 'In Transit'
#     DELIVERY_DELIVERED = 'Delivered'

#     DELIVERY_STATUS_CHOICES = [
#         (DELIVERY_PENDING, 'Pending'),
#         (DELIVERY_DISPATCHED, 'Dispatched'),
#         (DELIVERY_IN_TRANSIT, 'In Transit'),
#         (DELIVERY_DELIVERED, 'Delivered'),
#     ]

#     order = models.ForeignKey('Order', on_delete=models.CASCADE)
#     status = models.CharField(
#         max_length=20, choices=DELIVERY_STATUS_CHOICES, default=DELIVERY_PENDING)
#     location = models.CharField(max_length=100)
#     estimated_delivery_time = models.DateTimeField(null=True, blank=True)
#     delivery_person = models.ForeignKey(
#         Delivery, on_delete=models.SET_NULL, null=True)
