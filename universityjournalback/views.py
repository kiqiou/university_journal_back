from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from authentication.models import Course, Faculty, Group, TeacherProfile
from authentication.serializers import GroupSerializer, UserSerializer
from .models import Attendance, Discipline, Session, User
from .serializers import CourseSerializer, SessionSerializer, SessionWithAttendanceSerializer

@api_view(['GET'])
def get_attendance(request):
    try:
        course_id = request.query_params.get('course_id')
        group_id = request.query_params.get('group_id')

        qs = Session.objects.all()
        if course_id:
            qs = qs.filter(course_id=course_id)

        if group_id:
            qs = qs.filter(attendance__student__group_id=group_id).distinct()

        serializer = SessionWithAttendanceSerializer(qs, many=True, context={'group_id': group_id})
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def add_session(request):
    type = request.data.get('type')
    date = request.data.get('date')
    course_id = request.data.get('course_id')

    if not course_id or not type or not date:
        return Response({'error': 'Айди курса, тип и дата обязательны'}, status=400)

    try:
        course = Discipline.objects.prefetch_related('groups').filter(id=course_id).first()
        if not course:
            return Response({'error': 'Курс не найден'}, status=404)

        session = Session.objects.create(type=type, date=date, course=course)

        group_ids = course.groups.values_list('id', flat=True)
        students = User.objects.filter(group__id__in=group_ids, role__role='Студент')

        attendances = [
            Attendance(session=session, student=student, status='н', grade=None)
            for student in students
        ]
        Attendance.objects.bulk_create(attendances)

        return Response(SessionSerializer(session).data, status=201)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)
    
@api_view(['PATCH'])
def update_session(request, id):
    try:
        session = Session.objects.get(pk=id)
    except Session.DoesNotExist:
        return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data 

    if "date" in data:
        session.date = data["date"]
    if "type" in data:
        session.session_type = data["type"] 
    if "topic" in data:
        session.topic = data["topic"]

    session.save()
    return Response({"success": True}, status=status.HTTP_200_OK)
    
@api_view(['PUT'])
def update_attendance(request):
    session_id = request.data.get('session_id')
    student_id = request.data.get('student_id')
    status_value = request.data.get('status')
    grade_value = request.data.get('grade')

    if not session_id or not student_id:
        return Response({'error': 'ID сессии и ID студента обязательны'}, status=400)

    try:
        attendance = Attendance.objects.get(session_id=session_id, student_id=student_id)
    except Attendance.DoesNotExist:
        return Response({'error': 'Запись посещаемости не найдена'}, status=404)

    if status_value is not None:
        attendance.status = status_value
    if grade_value is not None:
        try:
            attendance.grade = int(grade_value)
        except ValueError:
            return Response({'error': 'Оценка должна быть числом'}, status=400)

    attendance.save(update_fields=['status', 'grade'])
    print(f"Обновление attendance: студент={attendance.student_id}, статус={attendance.status}, оценка={attendance.grade}")

    return Response({'success': True, 'message': 'Посещаемость обновлена'})


@api_view(['POST'])
def delete_session(request):
    session_id = request.data.get('session_id')

    if not session_id:
        return Response({'error': 'ID сессии обязателен'}, status=400)

    try:
        session = Session.objects.get(id=session_id)
        session.delete()
        return Response({'message': 'Сессия успешно удалена'}, status=200)
    except Session.DoesNotExist:
        return Response({'error': 'Сессия не найдена'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['POST'])
def get_teacher_list(request):
    try:
        teachers_list = User.objects.filter(role__role="Преподаватель")
        serializer = UserSerializer(teachers_list, many=True)
        return Response(serializer.data, status=201, content_type="application/json; charset=utf-8")
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)
    
@api_view(['POST'])
def get_student_list(request):
    try:
        student_list = User.objects.filter(role__role="Студент")
        serializer = UserSerializer(student_list, many=True)
        return Response(serializer.data, status=201, content_type="application/json; charset=utf-8")
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

@api_view(['PUT'])
def update_user(request, user_id):
    try:
        print("🔍 Получен user_id:", user_id)
        user = User.objects.get(id=user_id)
    except (User.DoesNotExist):
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    username = request.data.get('username')
    group_id = request.data.get('group_id')
    position = request.data.get('position')
    bio = request.data.get('bio')

    if username:
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
            group.student = user  
            group.save()
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

    if 'photo' in request.FILES:
        user.teacher_profile.photo = request.FILES['photo']
        user.teacher_profile.save()
    
    user.save()

    return Response({'message': 'User updated successfully'})

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
    
@api_view(['GET'])
def get_groups_list(request):
    try:
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)

@api_view(['POST'])
def add_group(request):
    print("📌 Полученные данные:", request.data)
    
    name = request.data.get('name')
    students_ids = request.data.get('students', [])
    faculty_id = request.data.get('faculty') 
    course_id = request.data.get('course')

    if not name:
        return Response({'error': 'Название группы обязательно'}, status=status.HTTP_400_BAD_REQUEST)
    if not faculty_id or not course_id:
        return Response({'error': 'Нужно указать факультет и курс'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        group = Group(name=name, faculty=Faculty.objects.get(id=faculty_id), course=Course.objects.get(id=course_id))
        group.save()

        valid_students = User.objects.filter(id__in=students_ids)
        for student in valid_students:
            student.group = group
            student.save()

        serializer = GroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except User.DoesNotExist:
        return Response({'error': 'Студент не найден'}, status=status.HTTP_404_NOT_FOUND)
    except Faculty.DoesNotExist:
        return Response({'error': 'Факультет не найден'}, status=status.HTTP_404_NOT_FOUND)
    except Course.DoesNotExist:
        return Response({'error': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_group(request):
    group_id = request.data.get('group_id')
    name = request.data.get('name')
    students_ids = request.data.get('students')
    faculty_id = request.data.get('faculty') 
    course_id = request.data.get('course')
    
    try:
        group = Group.objects.get(id=group_id)

        if name:
            group.name = name

        if students_ids is not None:
            User.objects.filter(group=group).update(group=None)
            valid_students = User.objects.filter(id__in=students_ids)
            for student in valid_students:
                student.group = group
                student.save()

        if faculty_id:
            valid_faculty = Faculty.objects.filter(id=faculty_id)
            group.faculty = valid_faculty.first()
        
        if course_id:
            valid_course = Course.objects.filter(id=course_id)
            group.course = valid_course.first()

        group.save()
        serializer = GroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Group.DoesNotExist:
        return Response({'error': 'Группа не найдена'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def delete_group(request):
    group_id = request.data.get('group_id')
    if not group_id:
        return Response({'error': 'ID группы обязателен'}, status=400)
    try:
        group = Group.objects.get(id=group_id)
        group.delete()
        return Response({'message': 'Группа успешно удалена'}, status=200)
    except Group.DoesNotExist:
        return Response({'error': 'Группане найдена'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def get_courses_list(request):
    try:
        courses_list = Discipline.objects
        serializer = CourseSerializer(courses_list, many=True)
        return Response(serializer.data, status=201, content_type="application/json; charset=utf-8")
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)
    
@api_view(['POST'])
def add_course(request):
    teachers_ids = request.data.get('teachers')
    groups_ids = request.data.get('groups') 
    name = request.data.get('name')

    if not name:
        return Response({'error': 'Название курса обязательно'}, status=status.HTTP_400_BAD_REQUEST)
    if not teachers_ids or not groups_ids:
        return Response({'error': 'Нужно указать преподавателей и группы'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        course = Discipline(name=name)

        course.save()
        valid_teachers = User.objects.filter(id__in=teachers_ids)
        valid_groups = Group.objects.filter(id__in=groups_ids)

        course.teachers.set(valid_teachers)
        course.groups.set(valid_groups)

        course.save()

        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Discipline.DoesNotExist:
        return Response({'error': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
def update_course(request):
    course_id = request.data.get('course_id')
    name = request.data.get('name')
    teachers_ids = request.data.get('teachers', [])
    groups_ids = request.data.get('groups', [])
    append_teachers = request.data.get('append_teachers', False)

    try:
        course = Discipline.objects.get(id=course_id)

        if name:
            course.name = name

        if teachers_ids:
            valid_teachers = User.objects.filter(id__in=teachers_ids)
    
            if append_teachers:
                course.teachers.add(*valid_teachers)
            else:
                course.teachers.set(valid_teachers)



        if groups_ids:
            valid_groups = Group.objects.filter(id__in=groups_ids)
            course.groups.set(valid_groups)

        course.save()
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Discipline.DoesNotExist:
        return Response({'error': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def delete_course(request):
    course_id = request.data.get('course_id')
    if not course_id:
        return Response({'error': 'ID дисциплины обязателен'}, status=400)
    try:
        course = Discipline.objects.get(id=course_id)
        course.delete()
        return Response({'message': 'Преподаватель успешно удален'}, status=200)
    except Discipline.DoesNotExist:
        return Response({'error': 'Преподаватель не найден'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)