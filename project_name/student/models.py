from django.db import models


# Create your models here.
class Student(models.Model):
    stuid = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=70)
    email = models.CharField(max_length=50)
    number = models.CharField(max_length=12, null=False, unique=True)
