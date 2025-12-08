from attestation.models import Attestation
from authentication.models.group import Course, Faculty, Group
from authentication.models.user import User
from authentication.serializers.group import GroupSerializer, GroupSimpleSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

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

        serializer = GroupSimpleSerializer(groups, many=True)
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
        group = Group(
            name=name,
            faculty=Faculty.objects.get(id=faculty_id),
            course=Course.objects.get(id=course_id)
        )
        group.save()

        valid_students = User.objects.filter(id__in=students_ids)
        students = sorted(valid_students, key=lambda s: s.username.lower())

        half = len(students) // 2
        for i, student in enumerate(students):
            student.subGroup = 1 if i < half else 2
            student.group = group
            student.save()

        disciplines = Discipline.objects.filter(groups=group)
        for discipline in disciplines:
            for student in valid_students:
                Attestation.objects.get_or_create(
                    discipline=discipline,
                    group=group,
                    student=student,
                    defaults={'result': ''}
                )

        sessions = Session.objects.filter(course__in=disciplines)
        attendances_to_create = []
        for session in sessions:
            for student in valid_students:
                if not Attendance.objects.filter(session=session, student=student).exists():
                    attendances_to_create.append(
                        Attendance(session=session, student=student, status='', grade=None)
                    )
        Attendance.objects.bulk_create(attendances_to_create)

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
            
        old_students = set(User.objects.filter(group=group).values_list('id', flat=True))

        if students_ids is not None:
            User.objects.filter(group=group).update(group=None, subGroup=None)

            valid_students = User.objects.filter(id__in=students_ids).order_by('username')
            half = len(valid_students) // 2

            for i, student in enumerate(valid_students):
                student.group = group
                student.subGroup = 1 if i < half else 2
                student.save()

            new_students_set = set(valid_students.values_list('id', flat=True))

            added_students = new_students_set - old_students
            removed_students = old_students - new_students_set

            disciplines = Discipline.objects.filter(groups=group)

            if added_students:
                new_students_qs = User.objects.filter(id__in=added_students)
                for discipline in disciplines:
                    for student in new_students_qs:
                        Attestation.objects.get_or_create(
                            discipline=discipline,
                            group=group,
                            student=student,
                            defaults={'result': ''}
                        )
                    
                sessions = Session.objects.filter(course__in=disciplines)
                attendances_to_create = []
                for session in sessions:
                    for student in new_students_qs:
                        if not Attendance.objects.filter(session=session, student=student).exists():
                            attendances_to_create.append(
                                Attendance(session=session, student=student, status='', grade=None)
                            )
                Attendance.objects.bulk_create(attendances_to_create)


            if removed_students:
                disciplines = Discipline.objects.filter(groups=group)

                Attestation.objects.filter(
                    group=group,
                    student_id__in=removed_students,
                    discipline__in=disciplines
                ).delete()

                sessions = Session.objects.filter(group=group, course__in=disciplines)
                Attendance.objects.filter(
                    session__in=sessions,
                    student_id__in=removed_students
                ).delete()

        if faculty_id:
            valid_faculty = Faculty.objects.filter(id=faculty_id).first()
            group.faculty = valid_faculty

        if course_id:
            valid_course = Course.objects.filter(id=course_id).first()
            group.course = valid_course

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