# Generated by Django 4.2.5 on 2023-11-15 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ware_app', '0004_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='customermodel',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
