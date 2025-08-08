from authentication.serializers.group import GroupSerializer
from authentication.serializers.user import UserSerializer
from journal.models.discipline import Discipline, DisciplinePlan
from rest_framework import serializers
    
class DisciplinePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplinePlan
        fields = ['id','discipline','type','hours_allocated','hours_per_session']

class DisciplineSerializer(serializers.ModelSerializer):
    teachers = UserSerializer(many=True)
    groups = GroupSerializer(many=True)
    plan_items = DisciplinePlanSerializer(many=True, source='plan_items.all')

    class Meta:
        model = Discipline
        fields = ['id', 'name', 'groups', 'teachers', 'plan_items', 'is_group_split', 'attestation_type']

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
