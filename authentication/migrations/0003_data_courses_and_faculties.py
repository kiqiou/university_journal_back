from django.db import migrations

def add_courses_and_faculties(apps, schema_editor):
    Course = apps.get_model('authentication', 'Course')
    Faculty = apps.get_model('authentication', 'Faculty')

    # Курсы
    courses_data = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
    ]
    for course_id, course_name in courses_data:
        Course.objects.update_or_create(id=course_id, defaults={'name': course_name})

    # Факультеты
    faculties_data = [
        (1, 'Экономический'),
        (2, 'Юридический'),
    ]
    for faculty_id, faculty_name in faculties_data:
        Faculty.objects.update_or_create(id=faculty_id, defaults={'name': faculty_name})

def remove_courses_and_faculties(apps, schema_editor):
    Course = apps.get_model('authentication', 'Course')
    Faculty = apps.get_model('authentication', 'Faculty')
    Course.objects.all().delete()
    Faculty.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_data_roles_and_admins'), 
    ]

    operations = [
        migrations.RunPython(add_courses_and_faculties, remove_courses_and_faculties),
    ]
