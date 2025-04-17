from rest_framework import serializers
from .models import User, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role'] 

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']


