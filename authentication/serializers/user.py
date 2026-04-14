from authentication.models.group import Group
from authentication.models.user import Role, StudentProfile, TeacherProfile, User
from authentication.serializers.group import SimpleGroupSerializer
from authentication.services.student_service import initialize_student_data
from rest_framework import serializers

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'role'] 

class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ['position', 'bio', 'photo']

class StudentProfileSerializer(serializers.ModelSerializer):
    group= SimpleGroupSerializer()
    class Meta:
        model= StudentProfile
        fields = ['group', 'isHeadman', 'subGroup']

class UserSerializer(serializers.ModelSerializer):
    teacher_profile = TeacherProfileSerializer(read_only=True)
    student_profile = StudentProfileSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'teacher_profile', 'student_profile', 'first_name', 'last_name', 'middle_name']

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role_id = serializers.IntegerField()

    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    middle_name = serializers.CharField(required=False)

    group_id = serializers.IntegerField(required=False)
    isHeadman = serializers.BooleanField(required=False)

    position = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)

    def validate(self, attrs):
        role = Role.objects.filter(id=attrs['role_id']).first()
        if not role:
            raise serializers.ValidationError("Некорректная роль")

        if role.role.lower() == 'студент' and not attrs.get('group_id'):
            raise serializers.ValidationError("Для студента нужна группа")

        if role.role.lower() == 'преподаватель' and not attrs.get('position'):
            raise serializers.ValidationError("Для преподавателя нужна должность")

        return attrs

    def create(self, validated_data):
        print("DATA:", validated_data)
        role = Role.objects.get(id=validated_data['role_id'])

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            middle_name=validated_data.get('middle_name', ''),
            role=role
        )

        if role.role.lower() == 'преподаватель':

            teacher_profile = TeacherProfile.objects.create(
                user=user,
                position=validated_data.get('position'),
                bio=validated_data.get('bio'),
            )

            request = self.context.get('request')
            if request and request.FILES.get('photo'):
                teacher_profile.photo = request.FILES['photo']
                teacher_profile.save()

        elif role.role.lower() == 'студент':
            group = Group.objects.get(id=validated_data['group_id'])
            student_profile = StudentProfile.objects.create(
                user=user,
                group=group,
                isHeadman=validated_data.get('isHeadman', False),
                subGroup=None  
            )
            initialize_student_data(student_profile)  
        return user

