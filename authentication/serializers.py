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

    def validate(self, data):
        role = data.get('role') or self.instance.role
        group = data.get('group') or self.instance.group

        if role and role.role != 'Студент' and group is not None:
            raise serializers.ValidationError('Только студент может быть в группе')
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            role = Role.objects.get(id=validated_data['role']['id'])
        )
        user.set_password(validated_data['password']) 
        user.save()
        return user