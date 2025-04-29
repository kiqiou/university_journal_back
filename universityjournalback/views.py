from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Attendance
from .serializers import AttendanceSerializer

@api_view(['GET', 'POST'])
def get_attendance(request):
    try:
        attendance_records = Attendance.objects.all() 
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data, status=201, content_type="application/json; charset=utf-8")
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)
    

