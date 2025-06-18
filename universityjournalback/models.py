from datetime import date, timedelta
from django.db import models
from authentication.models import User, Group

class Discipline(models.Model):
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
    
    course = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name="sessions")
    date = models.DateField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    topic = models.CharField(max_length=255, null=True)

class DisciplinePlan(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name="plan_items")
    hours_per_session = models.PositiveIntegerField(default=2) 
    type = models.CharField(max_length=50, choices=Session.TYPE_CHOICES)
    hours_allocated = models.PositiveIntegerField()

    @property
    def expected_sessions_count(self):
        return self.hours_allocated // self.hours_per_session

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('н', 'Отсутствовал'),
        ('п', 'Присутствовал'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Студент'})
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    grade = models.IntegerField(null=True, blank=True) 
