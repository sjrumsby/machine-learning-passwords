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
    tab_pressed     = models.BooleanField()
    enter_pressed   = models.BooleanField()
    total_time      = models.IntegerField()

class Key_Stroke(models.Model):
    user_signature  = models.ForeignKey(User_Signature)
    letter          = models.IntegerField()
    hold_time       = models.IntegerField()
    next_up_time    = models.IntegerField(null=True)
    next_down_time  = models.IntegerField(null=True)

