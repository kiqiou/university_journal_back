from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Role(models.Model):
    role = models.CharField(max_length=100)

class Faculty(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True,)

class Course(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True,)

class Group(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)
    
class TeacherProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='teacher_profile')
    position = models.CharField(max_length=255)
    bio = models.TextField()
    photo = models.ImageField(upload_to='photos/teachers/', null=True, blank=True) 
    

class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.TextField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    isHeadman = models.BooleanField(null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)
        super().save(*args, **kwargs)
    

