from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.

class user_data(models.Model):
    userName = models.TextField()
    userAccount = models.TextField()
    userPassword = models.TextField()
    friends = models.TextField(blank=True, null=True)

class message(models.Model):
    
    text = models.TextField(default='')
    since = models.TextField(default='')
    to = models.TextField(default='')
    add_time = models.DateTimeField(auto_now_add=True)
    
class user_key(models.Model):
    account = models.TextField()
    value = models.TextField()