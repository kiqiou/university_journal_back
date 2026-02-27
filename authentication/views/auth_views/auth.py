from journal.models.discipline import Discipline
from journal.serializers.discipline.discipline import DisciplineSerializer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from authentication.serializers.user import RegisterSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def register_user(request):
    serializer = RegisterSerializer(
        data=request.data,
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response(UserSerializer(user).data, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    try:
        user = request.user
        user_data = UserSerializer(user).data

        if user.role and user.role.role == 'Преподаватель':
            teacher_courses = Discipline.objects.filter(teachers=user)
            courses_data = DisciplineSerializer(teacher_courses, many=True).data
            user_data['courses'] = courses_data

        return Response(user_data, status = 200)
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=401)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "Успешный выход"}, status=status.HTTP_200_OK)
    


