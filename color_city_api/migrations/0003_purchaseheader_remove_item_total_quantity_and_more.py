# Generated by Django 4.2.5 on 2023-10-29 05:31

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
                ('date_created', models.DateTimeField(auto_now=True, null=True)),
                ('status', models.CharField(blank=True, default='UNPOSTED', max_length=100, null=True)),
                ('received_status', models.CharField(blank=True, default='PENDING', max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('removed', models.BooleanField(blank=True, default=False, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='color_city_api.branch')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='color_city_api.supplier')),
            ],
            options={
                'db_table': 'purchase_headers',
            },
        ),
        migrations.RemoveField(
            model_name='item',
            name='total_quantity',
        ),
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.AddField(
            model_name='item',
            name='brand_item',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='branch_name',
            field=models.CharField(default='SAMPLE', max_length=100),
        ),
        migrations.CreateModel(
            name='PurchaseLine',
            fields=[
                ('purchase_line_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('req_quantity', models.IntegerField()),
                ('received_quantity', models.IntegerField(default=0)),
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
        migrations.AddField(
            model_name='purchaseheader',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='color_city_api.user'),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('log_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('type', models.CharField(default='NONE', max_length=100)),
                ('type_id', models.IntegerField()),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('removed', models.BooleanField(blank=True, default=False, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='color_city_api.branch')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='color_city_api.user')),
            ],
            options={
                'db_table': 'logs',
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
