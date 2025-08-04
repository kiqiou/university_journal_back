from attestation.models import USR, Attestation
from rest_framework import serializers
from authentication.serializers.group import GroupSerializer
from authentication.serializers.user import UserSerializer
from journal.serializers.discipline.discipline import DisciplineSerializer

class USRSerializer(serializers.ModelSerializer):
    class Meta:
        model = USR
        fields = ['id', 'grade', 'attestation']

class AttestationSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    discipline = DisciplineSerializer()
    group = GroupSerializer()
    usr_items = USRSerializer(many=True) 
    class Meta:
        model = Attestation
        fields = ['id', 'student', 'discipline', 'group', 'average_score', 'usr_items', 'result', 'attestation_type',]

