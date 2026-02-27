from attestation.models import Attestation
from authentication.models.group import Course, Faculty, Group
from authentication.models.user import StudentProfile, User
from authentication.serializers.group import GroupSerializer, SimpleGroupSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from authentication.services.student_service import initialize_student_data
from journal.models.discipline import Discipline
from journal.models.session import Attendance, Session

@api_view(['POST'])
def get_groups_list(request):
    try:
        faculties = request.data.get("faculties", [])
        courses = request.data.get("courses", [])

        groups = Group.objects.all()

        if faculties:
            groups = groups.filter(faculty__name__in=faculties)
        if courses:
            groups = groups.filter(course_id__in=courses)
        
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)

@api_view(['GET'])
def get_groups_simple_list(request):
    try:
        groups = Group.objects.all()

        serializer = SimpleGroupSerializer(groups, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)

@api_view(['POST'])
def add_group(request):
    name = request.data.get('name')
    students_ids = request.data.get('students', [])
    faculty_id = request.data.get('faculty')
    course_id = request.data.get('course')

    if not name:
        return Response({'error': 'Название группы обязательно'}, status=status.HTTP_400_BAD_REQUEST)
    if not faculty_id or not course_id:
        return Response({'error': 'Нужно указать факультет и курс'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        group = Group.objects.create(
            name=name,
            faculty=Faculty.objects.get(id=faculty_id),
            course=Course.objects.get(id=course_id)
        )

        student_profiles = StudentProfile.objects.filter(user__id__in=students_ids)
        for sp in student_profiles:
            sp.group = group
            sp.save()

        for sp in student_profiles:
            initialize_student_data(sp)

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

        old_students = set(StudentProfile.objects.filter(group=group).values_list('user_id', flat=True))

        if students_ids is not None:
            StudentProfile.objects.filter(group=group).update(group=None, subGroup=None)

            student_profiles = StudentProfile.objects.filter(user__id__in=students_ids)
            for sp in student_profiles:
                sp.group = group
                sp.save()

            for sp in student_profiles:
                initialize_student_data(sp)

            removed_students = old_students - set(students_ids)
            if removed_students:
                disciplines = Discipline.objects.filter(groups=group)
                Attestation.objects.filter(
                    group=group,
                    student_id__in=removed_students,
                    discipline__in=disciplines
                ).delete()
                sessions = Session.objects.filter(course__in=disciplines)
                Attendance.objects.filter(
                    session__in=sessions,
                    student_id__in=removed_students
                ).delete()

        if faculty_id:
            group.faculty = Faculty.objects.get(id=faculty_id)

        if course_id:
            group.course = Course.objects.get(id=course_id)

        group.save()
        serializer = GroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Group.DoesNotExist:
        return Response({'error': 'Группа не найдена'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
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