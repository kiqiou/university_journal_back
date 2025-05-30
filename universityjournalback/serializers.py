from rest_framework import serializers
from .models import CoursePlan, Session, Attendance, Course
from authentication.serializers import GroupSerializer, UserSerializer

class CourseSerializer(serializers.ModelSerializer):
    teachers = UserSerializer(many=True)
    groups = GroupSerializer(many=True)
    class Meta:
        model = Course
        fields = ['id', 'name', 'groups', 'teachers']

class SessionSerializer(serializers.ModelSerializer):
    course = CourseSerializer(required=False, allow_null=True)
    class Meta:
        model = Session
        fields = ['id', 'course', 'date', 'type', 'topic']

class CoursePlanSerializer(serializers.ModelSerializer):
    expected_sessions_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CoursePlan
        fields = ['id', 'course', 'type', 'hours_allocated', 'expected_sessions_count']


class AttendanceSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    session = SessionSerializer()
    class Meta:
        model = Attendance
        fields = ['session', 'student', 'status', 'grade']