# Generated by Django 4.2.5 on 2023-10-19 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('color_city_api', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseHeader',
            fields=[
                ('purchase_header_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('transaction_type', models.CharField(max_length=100)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('payment_mode', models.CharField(max_length=100)),
                ('posted_status', models.CharField(default='UNPOSTED', max_length=100)),
                ('received_status', models.CharField(default='PENDING', max_length=100)),
                ('approval_status', models.CharField(default='PENDING', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('removed', models.BooleanField(blank=True, default=False, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='color_city_api.branch')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'purchase_headers',
            },
        ),
        migrations.CreateModel(
            name='PurchaseLine',
            fields=[
                ('purchase_line_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('req_quantity', models.IntegerField()),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=100)),
                ('status', models.CharField(default='NONE', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('removed', models.BooleanField(blank=True, default=False, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='color_city_api.item')),
                ('purchase_header', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='color_city_api.purchaseheader')),
            ],
            options={
                'db_table': 'purchase_lines',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('inventory_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('total_quantity', models.IntegerField()),
                ('holding_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('removed', models.BooleanField(blank=True, default=False, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='color_city_api.branch')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='color_city_api.item')),
            ],
            options={
                'db_table': 'inventory',
            },
        ),
    ]
