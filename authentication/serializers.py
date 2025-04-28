from rest_framework import serializers
from .models import User, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'role'] 

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)  
    password = serializers.CharField(write_only=True) 

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            role = Role.objects.get(id=validated_data['role']['id'])
        )
        user.set_password(validated_data['password']) 
        user.save()
        return user