from datetime import date, timedelta
from django.db import models
from authentication.models import User, Group
from universityjournalback import settings

class Discipline(models.Model):
    name = models.CharField(max_length=255)
    groups = models.ManyToManyField(Group, related_name='courses')
    teachers = models.ManyToManyField(User, limit_choices_to={'role': 'Преподаватель'})
    is_group_split = models.BooleanField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Session(models.Model):
    TYPE_CHOICES = [
        ('Лекция', 'Лекция'),
        ('Практика', 'Практика'),
        ('Семинар', 'Семинар'),
        ('Лабораторная', 'Лабораторная'),
        ('Аттестация', 'Аттестация'),
    ]
    
    course = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name="sessions")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="sessions")
    date = models.DateField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    topic = models.CharField(max_length=255, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DisciplinePlan(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name="plan_items")
    hours_per_session = models.PositiveIntegerField(default=2) 
    type = models.CharField(max_length=50, choices=Session.TYPE_CHOICES)
    hours_allocated = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def expected_sessions_count(self):
        return self.hours_allocated // self.hours_per_session

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