from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Role
from .serializers import UserSerializer
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def register_user(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        role_id = request.data.get('role_id')

        if not username or not password or not role_id:
            return Response({'error': 'Имя, пароль и ID роли обязательны'}, status=400)

        try:
            role_id = int(role_id)
        except ValueError:
            return Response({'error': 'ID роли должен быть числом'}, status=400)

        role = Role.objects.filter(id=role_id).first()
        if not role:
            return Response({'error': 'Некорректный ID роли'}, status=400)

        user = User(username=username, role=role)
        user.set_password(password) 
        user.save()

        return Response(UserSerializer(user).data, status=201)

    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)

@api_view(['POST'])
def login_user(request):

    try:
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        print(f"Полученные данные: {username}, {password}")

        user = User.objects.filter(username=username).first()
        print(f"user: {user}")
        print(f"Пароль валиден: {check_password(password, user.password) if user else 'user not found'}")

        if not user or not check_password(password, user.password):
            return Response({'error': 'Неверное имя пользователя или пароль'}, status=400)
        print(f"Сериализованные данные: {UserSerializer(user).data}")

        return Response({'message': 'Успешный вход', 'user': UserSerializer(user).data}, status=200)
    except Exception as e:
        print(f"Ошибка: {str(e)}") 
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "Успешный выход"}, status=status.HTTP_200_OK)

