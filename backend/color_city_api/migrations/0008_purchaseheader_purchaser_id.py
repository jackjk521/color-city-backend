# Generated by Django 4.2.5 on 2023-10-23 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('color_city_api', '0007_rename_approval_status_purchaseheader_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseheader',
            name='purchaser_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
