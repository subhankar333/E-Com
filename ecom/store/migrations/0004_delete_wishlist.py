# Generated by Django 4.2.4 on 2023-08-17 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_wishlist_product_wishlist_products'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]
