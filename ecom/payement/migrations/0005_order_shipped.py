# Generated by Django 5.0.7 on 2024-09-05 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payement', '0004_rename_shopping_address1_shippingaddress_shipping_address1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipped',
            field=models.BooleanField(default=False),
        ),
    ]
