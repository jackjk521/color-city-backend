## Steps

pip install virtualenv
virtualenv venv
venv\Scripts\activate
pip install djangorestframework markdown django-filter
django-admin startproject name
python manage.py runserver
python manage.py runserver port_number

Edit settings.py and add this 'rest_framework' under installed_apps

## Migrations

python manage.py makemigrations
python manage.py migrate

## To remove the initial tables created by django

Go to the migration file and set initial to false

## Shows the list of applied or not applied migrations

python manage.py showmigrations

## Remove Migrations

python manage.py makemigrations --colorcitydb

## pgAdmin SQL for dropping all tables

GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

## Moving data from a non sql but CSV file
# Note: foreign keys have _id attached automatically ie brand = brand_id


COPY table_name (column1, column2, ...) FROM 'path/to/your/csv/file.csv' DELIMITER ',' CSV HEADER;

COPY suppliers (supplier_name, contact_num, discount_rate, created_at, removed)
FROM 'C:\color_city_db\color_city_db - suppliers.csv'
DELIMITER ',' CSV HEADER;

COPY brands (supplier_id, brand_name, created_at, removed)
FROM 'C:\color_city_db\color_city_db - brands.csv'
DELIMITER ',' CSV HEADER;

COPY categories (category_name, created_at, removed)
FROM 'C:\color_city_db\color_city_db - categories.csv'
DELIMITER ',' CSV HEADER;

COPY items ( item_number, item_name, brand_id, category_id, unit, package, item_price_w_vat, item_price_wo_vat, retail_price, catalyst,  created_at, removed)
FROM 'C:\color_city_db\color_city_db - items.csv'
DELIMITER ',' CSV HEADER;


COPY users (branch_id, user_role, first_name, last_name, age,  created_at, removed)
FROM 'C:\color_city_db\color_city_db - users.csv'
DELIMITER ',' CSV HEADER;

COPY branches (branch_name, address, created_at, removed)
FROM 'C:\color_city_db\color_city_db - branches.csv'
DELIMITER ',' CSV HEADER;



For tables with foreign keys

ALTER TABLE child_table DISABLE TRIGGER ALL;

COPY command

ALTER TABLE child_table ENABLE TRIGGER ALL;

OR

python import_data.py "C:\color_city_db\color_city_db - suppliers.csv" Suppliers

# Add this to the import file to read the settings

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'color_city_backend.settings')

## Tips:

deactivate - to exit the (venv)
TO DO / CONTINUE
Configure databse in settings.py under DATABASES
pip freeze (to see all packages installed)

python manage.py startapp NAME_OF_table

## Notes:

Serializers help with translating between JSON, XML, and native Python objects.

## Flow:

Create models = tables to migrate
Create Serializers to transform JSON/XML or native Python objects
Create queries in the views.py
Add the queries to the urls.py (format ie /admin or /page_name) - MAIN
Add the specific queries to the urls.py (for CRUD and etc) - API

## Modal Field Types

BooleanField(**options)
CharField(max_length=None, **options)
DecimalField (max_digits=None, decimal_places=None, \*\*options)

DateTimeField (auto_now=False, auto_now_add=False, **options)
DateField (auto_now=False, auto_now_add=False, **options)

# auto_now (adds everytime the object is saved)

# auto_now_add (adds only when the object is created)

EmailField(max_length=254, **options)
FileField(upload_to='', storage=None, max_length=100, **options)
IntegerField(**options)
SlugField(max_length=50, **options)
TextField(**options)
UUIDField(**options)

# blank=True allows the field to be left blank. If False, the field must have a value.

# null=True allows the field to have a NULL database value. If False, the field must have a value.

## Relationships

# one to one relationship

.OneToOneField(table_name, on_delete=models.CASCADE)

# one to many relationship

.ForeignKey(
table_name,
on_delete=models.CASCADE,
verbose_name="readable",
)

# many to many relationship

.ManyToManyField(table_name)

# Table Naming

in the models.py;

class Meta:
db_table = 'custom_table_name'
