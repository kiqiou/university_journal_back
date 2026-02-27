from attestation.models import Attestation
from authentication.models.user import StudentProfile, TeacherProfile, User
from authentication.serializers.user import UserSerializer
from authentication.services.student_service import initialize_student_data
from journal.models.discipline import Discipline
from journal.models.session import Attendance, Session
from journal.serializers.discipline.discipline import DisciplineSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from authentication.models import Group

@api_view(['GET'])
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
        student_profiles = StudentProfile.objects.filter(group__id=group_id)
        students = [sp.user for sp in student_profiles]
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)

@api_view(['GET'])
def get_students_without_group(request):
    try:
        student_profiles = StudentProfile.objects.filter(group__isnull=True)
        students = [sp.user for sp in student_profiles]
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)

@api_view(['PUT'])
def update_user(request, user_id):
    try:
        user = User.objects.select_related(
            'teacher_profile',
            'student_profile'
        ).get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    username = request.data.get('username')
    group_id = request.data.get('group_id')
    position = request.data.get('position')
    bio = request.data.get('bio')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    middle_name = request.data.get('middle_name')
    isHeadman = request.data.get('isHeadman')

    if username and username != user.username:
        if User.objects.filter(username__iexact=username)\
                .exclude(id=user.id).exists():
            return Response(
                {'error': 'Пользователь с таким именем уже существует'},
                status=400
            )
        user.username = username
    
    if first_name is not None:
            user.first_name = first_name

    if last_name is not None:
        user.last_name = last_name

    if middle_name is not None:
        user.middle_name = middle_name

    if hasattr(user, 'teacher_profile'):
        teacher = user.teacher_profile

        if position is not None:
            teacher.position = position

        if bio is not None:
            teacher.bio = bio

        if 'photo' in request.FILES:
            teacher.photo = request.FILES['photo']

        teacher.save()

    if hasattr(user, 'student_profile'):
        student = user.student_profile
        group_changed = False

        if group_id:
            try:
                new_group = Group.objects.get(id=group_id)
                if student.group != new_group:
                    student.group = new_group
                    student.subGroup = None
                    group_changed = True
            except Group.DoesNotExist:
                return Response({'error': 'Group not found'}, status=404)

        if isHeadman is not None:
            try:
                student.isHeadman = bool(int(isHeadman))
            except (TypeError, ValueError):
                return Response({'error': 'Некорректный isHeadman'}, status=400)

        student.save()

        if group_changed:
            Attendance.objects.filter(student=user).delete()
            Attestation.objects.filter(student=user).delete()
            initialize_student_data(student)

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

@api_view(['DELETE'])
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
    

