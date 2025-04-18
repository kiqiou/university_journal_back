from django.db import models

class Role(models.Model):
    role = models.CharField(max_length=100)

class User(models.Model):
    username = models.CharField(max_length=100, null=False, blank=False)
    password = models.TextField(null=False, blank=False)
    role = models.ManyToManyField(Role)

