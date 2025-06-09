from rest_framework import serializers
from .models import Course, Faculty, User, Role, TeacherProfile, Role, Group

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'role'] 

class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ['position', 'bio', 'photo']

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name']

class GroupSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField() 
    faculty = FacultySerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    class Meta:
        model = Group
        fields = ['id', 'group_name', 'faculty', 'course', 'students']
    
    def get_students(self, obj):
        students = User.objects.filter(group=obj)
        return UserSerializer(students, many=True).data

class UserSerializer(serializers.ModelSerializer):
    teacher_profile = TeacherProfileSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    group = GroupSerializer(read_only=True) 

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'teacher_profile', 'group']

