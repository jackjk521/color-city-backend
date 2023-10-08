from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Todo(models.Model):
    task = models.CharField(max_length = 180)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    completed = models.BooleanField(default = False, blank = True)
    updated = models.DateTimeField(auto_now = True, blank = True)
 

    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)

    def __str__(self):
        return self.task
    
# class Teacher(models.Model):
#     name = models.CharField(max_length=80)
#     age = models.IntegerField()

# class MyModel(models.Model):
#     # name of the fk = where the FK is from , onDelete (delete all related entries as well)
#     another_model = models.ForeignKey(AnotherModel, on_delete=models.CASCADE) 