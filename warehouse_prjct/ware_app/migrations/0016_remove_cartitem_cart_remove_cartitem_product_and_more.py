# Generated by Django 4.2.5 on 2023-11-16 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ware_app', '0015_cart_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]