from authentication.models.user import User
from authentication.serializers.user import UserSerializer
from journal.models.discipline import Discipline
from journal.models.session import Attendance, Session
from journal.serializers.discipline.discipline import DisciplineSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from authentication.models import Group

@api_view(['POST'])
def get_teacher_list(request):
    try:
        teachers_list = User.objects.filter(role__role="Преподаватель")
        serializer = UserSerializer(teachers_list, many=True)
        data = serializer.data

        for item in data:
            user_id = item['id']
            user = User.objects.get(id=user_id)
            teacher_courses = Discipline.objects.filter(teachers=user)
            courses_data = DisciplineSerializer(teacher_courses, many=True).data
            item['courses'] = courses_data

        return Response(data, status=201, content_type="application/json; charset=utf-8")
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)
    
@api_view(['POST'])
def get_students_by_group(request):
    group_id = request.data.get('group_id')

    if not group_id:
        return Response({'error': 'ID группы обязателен'}, status=400)

    try:
        students = User.objects.filter(role__role="Студент", group__id=group_id)
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)

@api_view(['GET'])
def get_students_without_group(request):
    try:
        students = User.objects.filter(role__role="Студент", group__isnull=True)
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)

@api_view(['PUT'])
def update_user(request, user_id):
    try:
        print("🔍 Получен user_id:", user_id)
        user = User.objects.get(id=user_id)
    except (User.DoesNotExist):
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    username = request.data.get('username', '').strip()
    group_id = request.data.get('group_id')
    position = request.data.get('position')
    bio = request.data.get('bio')
    isHeadman = request.data.get('isHeadman')

    if username and username != user.username:
        if User.objects.filter(username__iexact=username).exclude(id=user.id).exists():
            return Response({'error': 'Пользователь с таким именем уже существует'}, status=status.HTTP_400_BAD_REQUEST)
        user.username = username
    
    if position:
        user.teacher_profile.position = position
        user.teacher_profile.save()
    
    if bio:
        user.teacher_profile.bio = bio
        user.teacher_profile.save()

    if group_id:
        try:
            group = Group.objects.get(id=group_id)

            old_group_id = user.group.id if user.group else None
            if old_group_id != group.id:
                user.group = group
                user.save()

            Attendance.objects.filter(student=user).delete()

            disciplines = Discipline.objects.filter(groups__id=group.id)
            sessions = Session.objects.filter(course__in=disciplines)

            attendances = [
                Attendance(session=session, student=user, status='', grade=None)
                for session in sessions
            ]
            Attendance.objects.bulk_create(attendances)

        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)


    if 'photo' in request.FILES:
        user.teacher_profile.photo = request.FILES['photo']
        user.teacher_profile.save()
    
        
    if 'isHeadman' in request.data:
        try: 
            user.isHeadman = bool(int(request.data['isHeadman']))
        except (TypeError, ValueError):
            return Response({'error': 'Некорректный isHeadman'}, status = 400)
    
    user.save()

    return Response({'message': 'User updated successfully'})

@api_view(['PUT'])
def update_teacher_disciplines(request):
    teacher_id = request.data.get('teacher_id')
    discipline_ids = request.data.get('discipline_ids', [])

    try:
        teacher = User.objects.get(id=teacher_id)

        for discipline in Discipline.objects.filter(teachers=teacher):
            discipline.teachers.remove(teacher)

        for discipline in Discipline.objects.filter(id__in=discipline_ids):
            discipline.teachers.add(teacher)

        return Response({"message": "Привязки обновлены"}, status=200)
    except User.DoesNotExist:
        return Response({"error": "Преподаватель не найден"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
def delete_user(request):
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'error': 'ID пользователя обязателен'}, status=400)
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({'message': 'Пользователь успешно удален'}, status=200)
    except User.DoesNotExist:
        return Response({'error': 'Пользователь не найден'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    

