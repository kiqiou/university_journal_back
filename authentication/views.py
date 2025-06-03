from email.headerregistry import Group
from rest_framework.decorators import api_view
from rest_framework.response import Response

from universityjournalback.models import Attendance, Discipline, Session
from universityjournalback.serializers import CourseSerializer
from .models import StudentProfile, TeacherProfile, User, Role
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
        group_id = request.data.get('group_id')
        position = request.data.get('position')
        bio = request.data.get('bio')

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

        if role.role.lower() == 'преподаватель':
            if not position or not bio:
                return Response({'error': 'Для преподавателя необходимы "position" и "bio"'}, status=400)
            TeacherProfile.objects.create(user=user, position=position, bio=bio)

        elif role.role.lower() == 'студент':
            if not group_id:
                return Response({'error': 'Для студента необходимо указать group_id'}, status=400)
            group = Group.objects.filter(id=group_id).first()
            if not group:
                return Response({'error': 'Некорректный group_id'}, status=400)
            
            sessions = Session.objects.filter(group_id=group_id)

            attendances = [
                Attendance(session=session, student=user, status='', grade=None)
                for session in sessions
                ]
            Attendance.objects.bulk_create(attendances)
            StudentProfile.objects.create(user=user, group=group)
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

        
        user_data = UserSerializer(user).data

        if user.role and user.role.role == 'Преподаватель':
            teacher_courses = Discipline.objects.filter(teachers=user)
            courses_data = CourseSerializer(teacher_courses, many=True).data
            user_data['courses'] = courses_data

        return Response({'message': 'Успешный вход','user': user_data}, status=200)
    
    except Exception as e:
        print(f"Ошибка: {str(e)}") 
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "Успешный выход"}, status=status.HTTP_200_OK)
    


