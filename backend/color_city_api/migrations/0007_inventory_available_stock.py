# Generated by Django 4.2.5 on 2023-11-02 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('color_city_api', '0006_alter_purchaseline_purchase_header'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='available_stock',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]