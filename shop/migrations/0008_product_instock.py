# Generated by Django 3.0.8 on 2020-10-20 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_orders_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='inStock',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
