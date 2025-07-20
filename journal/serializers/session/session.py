from journal.models.session import Attendance, Session
from journal.serializers.discipline.discipline import DisciplineSerializer
from rest_framework import serializers
from authentication.serializers.user import UserSerializer

class SessionWithAttendanceSerializer(serializers.ModelSerializer):
    attendances = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ['id', 'course', 'date', 'type', 'topic', 'attendances', 'subGroup']

    def get_attendances(self, obj):
        group_id = self.context.get('group_id')
        attendance_qs = Attendance.objects.filter(session=obj)

        if group_id:
            attendance_qs = attendance_qs.filter(student__group_id=group_id)

        return AttendanceSerializer(attendance_qs, many=True).data

class SessionSerializer(serializers.ModelSerializer):
    course = DisciplineSerializer(required=False, allow_null=True)
    class Meta:
        model = Session
        fields = ['id', 'course', 'date', 'type', 'topic', 'subGroup']

class AttendanceSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    modified_by = UserSerializer()
    session = SessionSerializer()
    class Meta:
        model = Attendance
        fields = ['session', 'student', 'status', 'grade', 'updated_at', 'modified_by']