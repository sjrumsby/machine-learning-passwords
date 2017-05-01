from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User_Status(models.Model):
    description     = models.CharField(max_length=32)

class Machine_User(models.Model):
    username        = models.CharField(max_length=16)
    password        = models.CharField(max_length=32)
    status          = models.ForeignKey(User_Status)

class User_Signature(models.Model):
    machine_user    = models.ForeignKey(Machine_User)
    attempt         = models.IntegerField()


