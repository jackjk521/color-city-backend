# Generated by Django 4.2.5 on 2023-10-10 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('color_city_api', '0002_alter_supplier_supplier_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='supplier_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]