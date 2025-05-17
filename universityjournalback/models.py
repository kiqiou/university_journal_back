from django.db import models
from authentication.models import User, Group

class Course(models.Model):
    name = models.CharField(max_length=255)
    groups = models.ManyToManyField(Group, related_name='courses')
    teachers = models.ManyToManyField(User, limit_choices_to={'role': 'Преподаватель'})

class Session(models.Model):
    TYPE_CHOICES = [
        ('Лекция', 'Лекция'),
        ('Практика', 'Практика'),
        ('Семинар', 'Семинар'),
        ('Лабораторная', 'Лабораторная'),
        ('Аттестация', 'Аттестация'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sessions")
    date = models.DateField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('н', 'Отсутствовал'),
        ('п', 'Присутствовал'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Студент'})
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    grade = models.IntegerField(null=True, blank=True) 
