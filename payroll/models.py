from __future__ import unicode_literals

from django.db import models

class Employee(models.Model):
    name=models.CharField(max_length=20)
    password=models.CharField(max_length=40)
    employee_id=models.CharField(max_length=20,unique=True)

