from rest_framework import serializers
from .models import Session, Attendance, Course
from authentication.serializers import UserSerializer

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name']

class SessionSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = Session
        fields = ['course', 'date', 'type']

class AttendanceSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    class Meta:
        model = Attendance
        fields = ['session', 'student', 'status', 'grade']