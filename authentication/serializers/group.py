from authentication.models.group import Course, Faculty, Group
from rest_framework import serializers

from authentication.models.user import StudentProfile

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name']

class GroupSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField() 
    faculty = FacultySerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'course', 'faculty', 'students']

    def get_students(self, obj):
        student_profiles = StudentProfile.objects.filter(group=obj)

        result = []
        for sp in student_profiles:
            user = sp.user
            if not user:
                continue

            result.append({
                'id': user.id,
                'username': user.username,
                'subGroup': sp.subGroup,
                'isHeadman': sp.isHeadman,
                'first_name': getattr(user, 'first_name', ''),
                'last_name': getattr(user, 'last_name', ''),
                'middle_name': getattr(user, 'middle_name', ''),
            })

        return result


class SimpleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']