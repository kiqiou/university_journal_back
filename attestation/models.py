from django.db import models

from authentication.models import Group, User
from journal.models.discipline import Discipline

class Attestation(models.Model):
    ATTESTATION_TYPE_CHOICES = [
        ('зачет', 'Зачет'),
        ('экзамен', 'Экзамен'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Студент'})
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='attestation_results')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='attestation_results')

    average_score = models.FloatField(null=True, blank=True)
    result = models.CharField(max_length=20, null=True, blank=True) 
    attestation_type = models.CharField(max_length=10, choices=ATTESTATION_TYPE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'discipline')

class USR(models.Model): #Управляемая самостоятельная работа
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Студент'})
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='usr_results')
    group = models.ForeignKey(Group, on_delete=models.CASCADE) 
    grade = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'discipline',)