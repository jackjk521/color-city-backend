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
COPY table_name (column1, column2, ...) FROM 'path/to/your/csv/file.csv' DELIMITER ',' CSV HEADER;


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
Add the queries to the urls.py

## Modal Field Types

BooleanField(**options)
CharField(max_length=None, **options)
DecimalField (max_digits=None, decimal_places=None, **options)
DateTimeField (auto_now=False, auto_now_add=False, **options)
DateField (auto_now=False, auto_now_add=False, **options)
EmailField(max_length=254, **options)
FileField(upload_to='', storage=None, max_length=100, **options)
IntegerField(**options)
SlugField(max_length=50, **options)
TextField(**options)
UUIDField(**options)


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

