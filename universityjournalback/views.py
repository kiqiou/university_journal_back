from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Attendance, Course, Session
from .serializers import AttendanceSerializer, SessionSerializer

@api_view(['GET', 'POST'])
def get_attendance(request):
    try:
        attendance_records = Attendance.objects.all() 
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data, status=201, content_type="application/json; charset=utf-8")
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)
    

@api_view(['GET', 'POST'])
def add_session(request):
    try:
        type = request.data.get('type')
        date = request.data.get('date')
        course_id = request.data.get('course_id')

        if not course_id or not type or not date:
            return Response({'error': 'Айди курса, тип и дата обязательны'}, status=400)

        course = Course.objects.filter(id=course_id).first()
        if not course:
            return Response({'error': 'Некорректный ID курса'}, status=400)

        session = Session(type = type, date = date, course = course)
        session.save()
        return Response(SessionSerializer(session).data, status=201,)
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)