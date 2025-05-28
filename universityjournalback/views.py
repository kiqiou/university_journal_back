from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from authentication.models import TeacherProfile
from authentication.serializers import UserSerializer
from .models import Attendance, Course, Session, User
from .serializers import AttendanceSerializer, SessionSerializer

@api_view(['GET', 'POST'])
def get_attendance(request):
    try:
        attendance_records = Attendance.objects.all() 
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data, status=201, content_type="application/json; charset=utf-8")
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)

@api_view(['POST'])
def add_session(request):
    type = request.data.get('type')
    date = request.data.get('date')
    course_id = request.data.get('course_id')

    if not course_id or not type or not date:
        return Response({'error': 'Айди курса, тип и дата обязательны'}, status=400)

    try:
        course = Course.objects.prefetch_related('groups').filter(id=course_id).first()
        if not course:
            return Response({'error': 'Курс не найден'}, status=404)

        session = Session.objects.create(type=type, date=date, course=course)
        group_ids = course.groups.values_list('id', flat=True)
        students = User.objects.filter(student_profile__group__id__in=group_ids,role__role='Студент')

        attendances = [
            Attendance(session=session, student=student, status='н', grade = None) 
            for student in students
        ]
        Attendance.objects.bulk_create(attendances)

        return Response(SessionSerializer(session).data, status=201)

    except Exception as e:
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
    student_id = request.data.get('student_id')  # 👈 добавь ID студента
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
    

@api_view(['PUT'])
def update_teacher(request, user_id):
    try:
        print("🔍 Получен user_id:", user_id)
        user = User.objects.get(id=user_id)
        teacher_profile = user.teacher_profile
    except (User.DoesNotExist, TeacherProfile.DoesNotExist):
        return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

    user.username = request.data.get('username', user.username)
    teacher_profile.position = request.data.get('position', teacher_profile.position)
    teacher_profile.bio = request.data.get('bio', teacher_profile.bio)

    user.save()
    teacher_profile.save()

    return Response({'message': 'Teacher updated successfully'})

@api_view(['POST'])
def delete_user(request):
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'error': 'ID сессии обязателен'}, status=400)
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({'message': 'Преподаватель успешно удален'}, status=200)
    except Session.DoesNotExist:
        return Response({'error': 'Преподаватель не найден'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
