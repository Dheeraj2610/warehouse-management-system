# Generated by Django 4.2.5 on 2023-11-20 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ware_app', '0030_order_admin_combined_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='dl_image',
            field=models.ImageField(null=True, upload_to='image/'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='dl_phone',
            field=models.IntegerField(null=True),
        ),
    ]
