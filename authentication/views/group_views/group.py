from authentication.models.group import Course, Faculty, Group
from authentication.models.user import User
from authentication.serializers.group import GroupSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_groups_list(request):
    try:
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=200, content_type="application/json; charset=utf-8")
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
        students = sorted(valid_students, key=lambda s: s.username.lower())

        half = len(students) // 2

        for i, student in enumerate(students):
            if i < half:
                student.subGroup = 1
            else:
                student.subGroup = 2
            student.save()


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