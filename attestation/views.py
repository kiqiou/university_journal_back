from attestation.models import USR, Attestation
from attestation.serializer import AttestationSerializer, USRSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_attestation(request):
    try:
        attestations = Attestation.objects.all()
        serializer = AttestationSerializer(attestations, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)
    
@api_view(['POST'])
def add_usr(request):
    attestation_id = request.data.get('attestation_id') 
    if not attestation_id:
        return Response({'Аттестация не найдена'}, status=400)
    try:
        attestation = Attestation.objects.get(id=attestation_id)
        usr = USR.objects.create(attestation=attestation,)
        serializer = USRSerializer(usr)
        return Response(serializer.data, status = 200)
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)

@api_view(['POST'])
def update_usr(request):
    attestation_id = request.data.get('attestation_id')
    grade = request.data.get('grade')

    if not attestation_id:
        return Response({'error': 'attestation_id обязателен'}, status=400)
    
    try:
        usr = USR.objects.get(attestation__id=attestation_id)

        if grade is not None:
            usr.grade = grade
            usr.save()

        serializer = USRSerializer(usr)

        return Response(serializer.data, status = 200)
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)

@api_view(['POST'])
def delete_usr(request):
    attestation_id = request.data.get('attestation_id')
    if not attestation_id:
        return Response({'error': 'attestation_id обязателен'}, status=400)
    try:
        usr = USR.objects.delete(attestation__id=attestation_id)
        return Response(status = 200)
    except Exception as e:
        return Response({'error': f'Ошибка: {str(e)}'}, status=500)




