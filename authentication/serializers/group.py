from authentication.models.group import Course, Faculty, Group
from rest_framework import serializers

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
        return [{'id': s.id, 'username': s.username, 'subGroup': s.subGroup} for s in obj.students.all()]