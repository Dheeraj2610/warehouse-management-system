# Generated by Django 4.2.5 on 2023-11-15 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ware_app', '0008_delivery_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ware_app.customermodel'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='delivery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ware_app.delivery'),
        ),
    ]
