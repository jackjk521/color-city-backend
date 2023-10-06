Steps
pip install virtualenv
virtualenv venv
venv\Scripts\activate
pip install djangorestframework markdown django-filter
django-admin startproject name
python manage.py runserver
python manage.py runserver port_number

<!-- Migrations  -->

python manage.py makemigrations
python manage.py migrate

<!-- To remove the initial tables created by django -->
Go to the migration file and set initial to false

<!-- Shows the list of applied or not applied migrations  -->
python manage.py showmigrations

<!-- Remove Migrations  -->
python manage.py makemigrations --colorcitydb

<!-- pgAdmin SQL for dropping all tables -->

GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

<!-- Moving data from a non sql but CSV file  -->
COPY table_name (column1, column2, ...) FROM 'path/to/your/csv/file.csv' DELIMITER ',' CSV HEADER;


Edit settings.py and add this 'rest_framework' under installed_apps

Tips:
deactivate - to exit the (venv)
TO DO / CONTINUE
Configure databse in settings.py under DATABASES
pip freeze (to see all packages installed)

python manage.py startapp NAME_OF_table
