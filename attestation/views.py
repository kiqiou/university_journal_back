from attestation.models import USR, Attestation
from attestation.serializer import AttestationSerializer, USRSerializer
from authentication.models.group import Group
from authentication.models.user import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_attestation(request):
    try:
        discipline_id = request.query_params.get('discipline_id')
        group_id = request.query_params.get('group_id')

        if not discipline_id or not group_id:
            return Response({'error': 'Не переданы discipline_id или group_id'}, status=400)

        attestations = Attestation.objects.filter(
            discipline_id=discipline_id,
            group_id=group_id,
        )

        serializer = AttestationSerializer(attestations, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)   

@api_view(['POST'])
def update_attestation(request):
    attestation_id = request.data.get('attestation_id')
    average_score = request.data.get('average_score')
    result = request.data.get('result')

    if not attestation_id:
        return Response({'error': 'attestation_id/usr_id обязателен'}, status=400)
    
    try:
        attestation=Attestation.objects.get(id=attestation_id)

        if average_score is not None:
            attestation.average_score = average_score
            attestation.save()
        
        if result is not None:
            attestation.result=result
            attestation.save()

        serializer = AttestationSerializer(attestation)

        return Response(serializer.data, status = 200)
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)
    
@api_view(['POST'])
def add_usr(request):
    group_id = request.data.get('group_id') 
    discipline_id = request.data.get('discipline_id')

    if not group_id or not discipline_id:
        return Response({'error': 'Не переданы group_id или discipline_id'}, status=400)

    try:
        group = Group.objects.get(id=group_id)
        students = User.objects.filter(group=group)

        created_usr_list = []

        for student in students:
            attestation = Attestation.objects.get(
                student=student,
                group_id=group_id,
                discipline_id=discipline_id,
            )
            usr = USR.objects.create(attestation=attestation)
            created_usr_list.append(usr)

        serializer = USRSerializer(created_usr_list, many=True)
        return Response(serializer.data, status=200)

    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)

@api_view(['POST'])
def update_usr(request):
    usr_id = request.data.get('usr_id')
    grade = request.data.get('grade')

    if not usr_id:
        return Response({'error': 'usr_id обязателен'}, status=400)
    
    try:
        usr = USR.objects.get(id=usr_id)

        if grade is not None:
            usr.grade = grade
            usr.save()

        serializer = USRSerializer(usr)

        return Response(serializer.data, status = 200)
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)

@api_view(['POST'])
def delete_usr(request):
    position = request.data.get('position') 
    group_id = request.data.get('group_id')
    discipline_id = request.data.get('discipline_id')

    if position is None or group_id is None or discipline_id is None:
        return Response({'error': 'position, group_id и discipline_id обязательны'}, status=400)

    try:
        attestations = Attestation.objects.filter(
            group_id=group_id,
            discipline_id=discipline_id
        )

        deleted_count = 0
        for att in attestations:
            usr_items = list(att.usr_items.order_by('id'))
            if 0 <= int(position) < len(usr_items):
                usr_to_delete = usr_items[int(position)]
                usr_to_delete.delete()
                deleted_count += 1

        return Response({'deleted': deleted_count}, status=200)

    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)





