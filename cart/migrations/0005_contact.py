# Generated by Django 3.2.2 on 2021-05-20 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_remove_wishlist_added_to_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=400)),
                ('message', models.TextField()),
            ],
        ),
    ]
