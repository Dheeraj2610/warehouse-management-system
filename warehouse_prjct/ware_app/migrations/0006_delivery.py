# Generated by Django 4.2.5 on 2023-11-15 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ware_app', '0005_customermodel_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dl_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('dl_email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
    ]
