from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

@api_view(['GET'])
def get_first_user(request):
    user = User.objects.first()  # Получаем первого пользователя
    if user:
        serializer = UserSerializer(user)
        return Response(serializer.data)
    return Response({'error': 'Нет пользователей в базе'}, status=404)
