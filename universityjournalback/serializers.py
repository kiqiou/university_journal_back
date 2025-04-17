from rest_framework import serializers
from .models import User
from rest_framework.decorators import api_view

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']
