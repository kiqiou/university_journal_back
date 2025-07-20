from django.db import models

class Faculty(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True,)

class Course(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True,)

class Group(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)