from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Group(models.Model):
    group_name = models.CharField(max_length=100, null=False, blank=False, unique=True)

class Role(models.Model):
    role = models.CharField(max_length=100)

class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.TextField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)
        super().save(*args, **kwargs)
    
class TeacherProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='teacher_profile')
    position = models.CharField(max_length=255)
    bio = models.TextField()

class StudentProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='student_profile')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
