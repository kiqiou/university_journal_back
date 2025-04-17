from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Role
from .serializers import UserSerializer
from django.http import JsonResponse

@api_view(['GET', 'POST'])
def add_role_to_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        
        # Если метод GET, возвращаем данные пользователя с ролями в правильной кодировке
        if request.method == 'GET':
            return JsonResponse(UserSerializer(user).data, json_dumps_params={'ensure_ascii': False})

        # Если POST, обновляем роли пользователя
        role_ids = request.data.get('role', [])
        roles = Role.objects.filter(id__in=role_ids)
        user.role.set(roles)
        return JsonResponse(UserSerializer(user).data, json_dumps_params={'ensure_ascii': False})

    except User.DoesNotExist:
        return Response({'error': 'Пользователь не найден'}, status=404)


