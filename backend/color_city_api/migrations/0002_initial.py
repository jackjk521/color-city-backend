# Generated by Django 4.2.5 on 2023-10-18 08:50

import color_city_api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('color_city_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('branch_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('branch_name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('removed', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'db_table': 'branches',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('brand_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('brand_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('removed', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'brands',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('category_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('removed', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('supplier_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('supplier_name', models.CharField(max_length=255)),
                ('contact_num', models.CharField(max_length=15)),
                ('discount_rate', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('removed', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'suppliers',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('item_number', models.CharField(max_length=20, unique=True)),
                ('item_name', models.CharField(max_length=255)),
                ('total_quantity', models.IntegerField()),
                ('unit', models.IntegerField()),
                ('package', models.CharField(max_length=255)),
                ('item_price_w_vat', models.DecimalField(decimal_places=2, max_digits=20)),
                ('item_price_wo_vat', models.DecimalField(decimal_places=2, max_digits=20)),
                ('retail_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('catalyst', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('removed', models.BooleanField(blank=True, default=False, null=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='color_city_api.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='color_city_api.category')),
            ],
            options={
                'db_table': 'items',
            },
        ),
        migrations.AddField(
            model_name='brand',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='color_city_api.supplier'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('user_role', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('removed', models.BooleanField(blank=True, default=False, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='color_city_api.branch')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
