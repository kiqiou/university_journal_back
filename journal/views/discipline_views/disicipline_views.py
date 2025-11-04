from authentication.models import Group, User
from attestation.models import Attestation
from journal.models.discipline import Discipline, DisciplinePlan
from journal.serializers.discipline.discipline import DisciplineSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import traceback

@api_view(['GET'])
def get_discipline_list(request):
    try:
        disciplines = Discipline.objects.all()
        serializer = DisciplineSerializer(disciplines, many=True)
        return Response(serializer.data, status=200, content_type="application/json; charset=utf-8")
    except Exception as e:
        print("Ошибка в get_discipline_list:")
        traceback.print_exc()
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)
    
@api_view(['POST'])
def add_discipline(request):
    print("REQUEST DATA:", request.data)
    teachers_ids = request.data.get('teachers')
    groups_ids = request.data.get('groups') 
    name = request.data.get('name')
    is_group_split = request.data.get('is_group_split')
    plan_items = request.data.get('plan_items', [])
    attestation_type = request.data.get('attestation_type')

    if not name:
        return Response({'error': 'Название дисциплины обязательно'}, status=status.HTTP_400_BAD_REQUEST)
    if not teachers_ids or not groups_ids:
        return Response({'error': 'Нужно указать преподавателей и группы'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        discipline = Discipline.objects.create(name=name)

        valid_teachers = User.objects.filter(id__in=teachers_ids)
        valid_groups = Group.objects.filter(id__in=groups_ids)

        discipline.teachers.set(valid_teachers)
        discipline.groups.set(valid_groups)
        discipline.is_group_split = is_group_split
        discipline.attestation_type=attestation_type
        discipline.save() 

        try:
            for group_id in groups_ids:
                group = Group.objects.get(id=group_id)
                students = User.objects.filter(group=group)
                for student in students:
                    attestation = Attestation.objects.create(
                        discipline=discipline,
                        group=group,
                        student=student,
                        result='',
                        )
                    print(attestation)
                    attestation.save()
        except Exception as e:
            print("❌ Ошибка:")
            traceback.print_exc()

        for item in plan_items:
            print("Plan item:", item)
            DisciplinePlan.objects.create(
                discipline=discipline,
                type=item.get('type'),
                hours_allocated=int(item.get('hours_allocated') or 0),
                hours_per_session=int(item.get('hours_per_session', 2))
            )

        serializer = DisciplineSerializer(discipline)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
def update_discipline(request):
    discipline_id = request.data.get('course_id')
    name = request.data.get('name')
    is_group_split = request.data.get('is_group_split')
    teachers_ids = request.data.get('teachers', [])
    groups_ids = request.data.get('groups', [])
    plan_items = request.data.get('plan_items', None)
    append_teachers = request.data.get('append_teachers', False)
    attestation_type = request.data.get('attestation_type')

    try:
        discipline = Discipline.objects.get(id=discipline_id)

        if name:
            discipline.name = name

        if 'is_group_split' in request.data:
            discipline.is_group_split = is_group_split

        if 'teachers' in request.data:
            valid_teachers = User.objects.filter(id__in=teachers_ids)
            if append_teachers:
                discipline.teachers.add(*valid_teachers)
            else:
                discipline.teachers.set(valid_teachers)

        if 'groups' in request.data:
            old_groups = set(discipline.groups.all().values_list('id', flat=True))
            new_groups = set(groups_ids)

            added_groups = new_groups - old_groups
            for group_id in added_groups:
                group = Group.objects.get(id=group_id)
                students = User.objects.filter(group=group)
                for student in students:
                    exists = Attestation.objects.filter(
                        student=student,
                        group=group,
                        discipline=discipline
                    ).exists()
                    if not exists:
                        Attestation.objects.create(
                            discipline=discipline,
                            group=group,
                            student=student,
                            result=''
                        )
            valid_groups = Group.objects.filter(id__in=groups_ids)
            discipline.groups.set(valid_groups)

        
        if 'attestation_type' in request.data:
            discipline.attestation_type=attestation_type
            discipline.save()

        if plan_items is not None:
            discipline.plan_items.all().delete()
            for item in plan_items:
                DisciplinePlan.objects.create(
                    discipline=discipline,
                    type=item['type'],
                    hours_allocated=item['hours_allocated'],
                    hours_per_session=item.get('hours_per_session', 2)
                )

        discipline.save()
        serializer = DisciplineSerializer(discipline)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Discipline.DoesNotExist:
        return Response({'error': 'Дисциплина не найдена'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_discipline(request):
    discipline_id = request.data.get('course_id')
    if not discipline_id:
        return Response({'error': 'ID дисциплины обязателен'}, status=400)
    try:
        discipline = Discipline.objects.get(id=discipline_id)
        discipline.delete()
        return Response({'message': 'Дисциплина успешно удалена'}, status=200)
    except Discipline.DoesNotExist:
        return Response({'error': 'Дисциплина не найдеа'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)