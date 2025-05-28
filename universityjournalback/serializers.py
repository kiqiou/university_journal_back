from rest_framework import serializers
from .models import Session, Attendance, Course
from authentication.serializers import UserSerializer

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name']

class SessionSerializer(serializers.ModelSerializer):
    course = CourseSerializer(required=False, allow_null=True)
    class Meta:
        model = Session
        fields = ['id', 'course', 'date', 'type', 'topic']

class AttendanceSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    session = SessionSerializer()
    class Meta:
        model = Attendance
        fields = ['session', 'student', 'status', 'grade']