from rest_framework import serializers
from .models import User, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role']

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=True, read_only=True)  
    password = serializers.CharField(write_only=True) 

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']

    def create(self, validated_data):
        """Создание нового пользователя с зашифрованным паролем"""
        password = validated_data.pop('password') 
        user = User.objects.create(**validated_data)
        user.set_password(password)  
        user.save() 
        return user

    def update(self, instance, validated_data):
        """Обновление существующего пользователя с зашифрованным паролем"""
        password = validated_data.pop('password', None)  
        if password:
            instance.set_password(password) 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)  
        instance.save() 
        return instance

