Steps
pip install virtualenv
virtualenv venv
venv\Scripts\activate
pip install djangorestframework markdown django-filter
django-admin startproject name 
python manage.py runserver
Edit settings.py and add this 'rest_framework' under installed_apps

Tips:
deactivate - to exit the (venv)
TO DO / CONTINUE
Configure databse in settings.py under DATABASES

python manage.py startapp NAME_OF_table 