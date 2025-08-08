from django.db import models

from authentication.models import Group, User
from journal.models.discipline import Discipline

class Attestation(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Студент'})
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='attestation_results')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='attestation_results')

    average_score = models.FloatField(null=True, blank=True)
    result = models.CharField(max_length=20, null=True, blank=True) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'discipline')

class USR(models.Model):
    attestation = models.ForeignKey(Attestation, related_name='usr_items', on_delete=models.CASCADE)
    grade = models.PositiveIntegerField(null=True, blank=True)
