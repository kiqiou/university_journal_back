from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(username, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)


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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class TeacherProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='teacher_profile')
    position = models.CharField(max_length=255)
    bio = models.TextField()
    photo = models.ImageField(upload_to='photos/teachers/', null=True, blank=True) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    password = models.TextField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    isHeadman = models.BooleanField(null=True)

    is_active = models.BooleanField(default=True)  # обязательно
    is_staff = models.BooleanField(default=False)  # обязательно

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)
        super().save(*args, **kwargs)

    

