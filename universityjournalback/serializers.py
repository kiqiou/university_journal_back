from rest_framework import serializers
from .models import DisciplinePlan, Session, Attendance, Discipline
from authentication.serializers import GroupSerializer, UserSerializer

class SessionWithAttendanceSerializer(serializers.ModelSerializer):
    attendances = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ['id', 'course', 'date', 'type', 'topic', 'attendances']

    def get_attendances(self, obj):
        group_id = self.context.get('group_id')
        attendance_qs = Attendance.objects.filter(session=obj)

        if group_id:
            attendance_qs = attendance_qs.filter(student__group_id=group_id)

        return AttendanceSerializer(attendance_qs, many=True).data
    
class DisciplinePlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = DisciplinePlan
        fields = ['id','discipline','type','hours_allocated','hours_per_session', 'is_group_split']

class DisciplineSerializer(serializers.ModelSerializer):
    teachers = UserSerializer(many=True)
    groups = GroupSerializer(many=True)
    plan_items = DisciplinePlanSerializer(many=True, source='plan_items.all')

    class Meta:
        model = Discipline
        fields = ['id', 'name', 'groups', 'teachers', 'plan_items']

    def create(self, validated_data):
        plan_data = validated_data.pop('plan_items')
        discipline = Discipline.objects.create(**validated_data)
        for plan in plan_data:
            DisciplinePlan.objects.create(discipline=discipline, **plan)
        return discipline

    def update(self, instance, validated_data):
        plan_data = validated_data.pop('plan_items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if plan_data is not None:
            instance.plan_items.all().delete()
            for plan in plan_data:
                DisciplinePlan.objects.create(discipline=instance, **plan)

        return instance

class SessionSerializer(serializers.ModelSerializer):
    course = DisciplineSerializer(required=False, allow_null=True)
    class Meta:
        model = Session
        fields = ['id', 'course', 'date', 'type', 'topic']

class AttendanceSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    modified_by = UserSerializer()
    session = SessionSerializer()
    class Meta:
        model = Attendance
        fields = ['session', 'student', 'status', 'grade', 'updated_at', 'modified_by']