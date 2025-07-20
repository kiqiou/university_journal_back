from authentication.models.user import Role, TeacherProfile, User
from authentication.serializers.group import GroupSerializer
from rest_framework import serializers

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'role'] 

class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ['position', 'bio', 'photo']

class UserSerializer(serializers.ModelSerializer):
    teacher_profile = TeacherProfileSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    group = GroupSerializer(read_only=True) 

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'teacher_profile', 'group', 'isHeadman', 'subGroup']

