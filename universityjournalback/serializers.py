from rest_framework import serializers
from .models import CoursePlan, Session, Attendance, Discipline
from authentication.serializers import GroupSerializer, UserSerializer

class CourseSerializer(serializers.ModelSerializer):
    teachers = UserSerializer(many=True)
    groups = GroupSerializer(many=True)
    class Meta:
        model = Discipline
        fields = ['id', 'name', 'groups', 'teachers']

class SessionSerializer(serializers.ModelSerializer):
    course = CourseSerializer(required=False, allow_null=True)
    class Meta:
        model = Session
        fields = ['id', 'course', 'date', 'type', 'topic']

class AttendanceForSessionSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    class Meta:
        model = Attendance
        fields = ['student', 'status', 'grade']

class SessionWithAttendanceSerializer(serializers.ModelSerializer):
    attendances = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ['id', 'course', 'date', 'type', 'topic', 'attendances']

    def get_attendances(self, obj):
        attendance_qs = Attendance.objects.filter(session=obj)
        return AttendanceForSessionSerializer(attendance_qs, many=True).data


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