
from authentication.models import User
from authentication.models.group import Group
from django.db import models


class Discipline(models.Model):
    name = models.CharField(max_length=255)
    groups = models.ManyToManyField(Group, related_name='courses')
    teachers = models.ManyToManyField(User, limit_choices_to={'role': 'Преподаватель'})
    is_group_split = models.BooleanField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DisciplinePlan(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name="plan_items")
    hours_per_session = models.PositiveIntegerField(default=2) 
    type = models.CharField(max_length=50,)
    hours_allocated = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def expected_sessions_count(self):
        return self.hours_allocated // self.hours_per_session
