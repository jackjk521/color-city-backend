from django.db import models

# Create your models here.
class Teacher(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField()

class MyModel(models.Model):
    # name of the fk = where the FK is from , onDelete (delete all related entries as well)
    another_model = models.ForeignKey(AnotherModel, on_delete=models.CASCADE) 