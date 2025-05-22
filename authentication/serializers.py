from rest_framework import serializers
from .models import User, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'role'] 

from rest_framework import serializers
from .models import User, TeacherProfile, StudentProfile, Role, Group

class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ['position', 'bio']

class StudentProfileSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.group_name', read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['group', 'group_name']

class UserSerializer(serializers.ModelSerializer):
    teacher_profile = TeacherProfileSerializer(read_only=True)
    student_profile = StudentProfileSerializer(read_only=True)
    role = RoleSerializer(read_only=True)  # ⬅️ Здесь возвращаем весь объект

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'teacher_profile', 'student_profile']
