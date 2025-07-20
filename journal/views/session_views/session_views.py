from django.utils import timezone
from authentication.models import User
from journal.models.discipline import Discipline
from journal.models.session import Attendance, Session
from journal.serializers.session.session import SessionSerializer, SessionWithAttendanceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
def get_attendance(request):
    try:
        course_id = request.query_params.get('course_id')
        group_id = request.query_params.get('group_id')

        qs = Session.objects.all()
        if course_id:
            qs = qs.filter(course_id=course_id)
        if group_id:
            qs = qs.filter(group_id=group_id) 

        serializer = SessionWithAttendanceSerializer(qs, many=True, context={'group_id': group_id})  
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def add_session(request):
    type = request.data.get('type')
    date = request.data.get('date')
    course_id = request.data.get('course_id')
    group_id = request.data.get('group_id')
    subGroup = request.data.get('subGroup')

    if not course_id or not type or not date or not group_id:
        return Response({'error': 'Айди курса, тип, дата и группа обязательны'}, status=400)

    try:
        discipline = Discipline.objects.prefetch_related('groups').filter(id=course_id).first()
        if not discipline:
            return Response({'error': 'Курс не найден'}, status=404)

        session = Session.objects.create(
            type=type,
            date=date,
            course=discipline,
            group_id=group_id,
            subGroup=subGroup,
        )

        group_ids = discipline.groups.values_list('id', flat=True)
        students = User.objects.filter(group__in=discipline.groups.all(),role__role='Студент')

        attendances = [
            Attendance(session=session, student=student, status='', grade=None)
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
        session.type = data["type"]
    if "topic" in data:
        session.topic = data["topic"]

    if "subGroup" in data:
        sub_group_value = session.subGroup 
        print(sub_group_value)
        print(session.subGroup)
        raw_value = data["subGroup"]
        if raw_value in [None, '', 'null']:
            sub_group_value = None
        else:
            try:
                sub_group_value = int(raw_value)
            except (TypeError, ValueError):
                return Response({"error": "Invalid subGroup value"}, status=status.HTTP_400_BAD_REQUEST)

        if session.subGroup != sub_group_value:
            session.subGroup = sub_group_value

    session.save()

    return Response({"success": True}, status=status.HTTP_200_OK)

    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
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

    fields_to_update = []

    if status_value is not None:
        attendance.status = status_value
        fields_to_update.append('status')

    if grade_value is not None:
        try:
            attendance.grade = int(grade_value)
            fields_to_update.append('grade')
        except ValueError:
            return Response({'error': 'Оценка должна быть числом'}, status=400)

    attendance.modified_by = request.user
    attendance.updated_at = timezone.now()
    fields_to_update.extend(['modified_by', 'updated_at'])

    attendance.save(update_fields=fields_to_update)
    print(f"UTC time: {attendance.updated_at} ({attendance.updated_at.tzinfo})")
    print(f"Local time: {timezone.localtime(attendance.updated_at)}")
    print(f"Обновление attendance: студент={attendance.student_id}, статус={attendance.status}, оценка={attendance.grade}, изменено={request.user.username}")

    return Response({
    'success': True,
    'message': 'Посещаемость обновлена',
    'modified_by': request.user.username,
    'updated_at': timezone.localtime(attendance.updated_at).isoformat(),
    })

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
