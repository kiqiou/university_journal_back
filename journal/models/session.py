from authentication.models import Group, User
from journal.models.discipline import Discipline
from universityjournalback import settings
from django.db import models

class Session(models.Model):
    TYPE_CHOICES = [
        ('Лекция', 'Лекция'),
        ('Практика', 'Практика'),
        ('Семинар', 'Семинар'),
        ('Лабораторная', 'Лабораторная'),
        ('УСР', 'УСР'),
    ]
    
    course = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name="sessions")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="sessions")
    date = models.DateField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    topic = models.CharField(max_length=255, null=True)
    subGroup = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('ув', 'Отсутствовал по уважительной причине'),
        ('неув', 'Отсутствовал по неуважительной причине'),
        (' ', 'Присутствовал')
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Студент'})
    status = models.CharField(max_length=4, choices=STATUS_CHOICES)
    grade = models.IntegerField(null=True, blank=True) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='modified_attendances'
    )