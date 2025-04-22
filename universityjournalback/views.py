from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Role
from .serializers import UserSerializer
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

@api_view(['GET', 'POST'])
def add_role_to_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        
        if request.method == 'GET':
            return JsonResponse(UserSerializer(user).data, json_dumps_params={'ensure_ascii': False})

        role_ids = request.data.get('role', [])
        roles = Role.objects.filter(id__in=role_ids)
        user.role.set(roles)
        return JsonResponse(UserSerializer(user).data, json_dumps_params={'ensure_ascii': False})

    except User.DoesNotExist:
        return Response({'error': 'Пользователь не найден'}, status=404)

@api_view(['POST'])
def register_user(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        role_ids = request.data.get('role_ids', [])

        if not username or not password:
            return Response({'error': 'Имя и пароль обязательны'}, status=400)

        # Создание нового пользователя (без хеширования здесь!)
        user = User(username=username, password=password)
        user.save()  # Здесь произойдёт правильное хеширование

        # Добавление ролей
        roles = Role.objects.filter(id__in=role_ids)
        if not roles:
            return Response({'error': 'Некорректные ID ролей'}, status=400)

        user.role.set(roles)
        user.save()

        return Response(UserSerializer(user).data, status=201)

    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)

@api_view(['POST'])
def login_user(request):

    try:
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        print(f"Полученные данные: {username}, {password}")  # Логирование

        user = User.objects.filter(username=username).first()
        print(f"user: {user}")
        print(f"Пароль валиден: {check_password(password, user.password) if user else 'user not found'}")

        if not user or not check_password(password, user.password):
            return Response({'error': 'Неверное имя пользователя или пароль'}, status=400)

        return Response({'message': 'Успешный вход', 'user': UserSerializer(user).data}, status=200)
    except Exception as e:
        print(f"Ошибка: {str(e)}")  # Логирование ошибки
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)



