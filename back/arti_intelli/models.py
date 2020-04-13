from django.db import models

# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=5)
    group = models.CharField(max_length=10)
    area = models.CharField(max_length=10)
    class_num = models.CharField(max_length=10)
    image = models.CharField(max_length=200)
    birthday = models.CharField(max_length=8)
    login_id = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    day_in = models.DateTimeField(auto_now_add=True)
    day_out = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

