# Generated by Django 3.2.2 on 2021-05-19 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='added_to_cart',
        ),
    ]
