from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_roles_and_users(apps, schema_editor):
    Role = apps.get_model('authentication', 'Role')
    User = apps.get_model('authentication', 'User')
    Course = apps.get_model('authentication', 'Course')
    Faculty = apps.get_model('authentication', 'Faculty')

    roles_data = [
        (1, 'Преподаватель'),
        (2, 'Администратор 1'),
        (3, 'Администратор 2'),
        (4, 'Декан'),
        (5, 'Студент'),
    ]
    for role_id, role_name in roles_data:
        Role.objects.update_or_create(id=role_id, defaults={'role': role_name})
    
    courses_data = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    
    ]
    for course_id, course_name in courses_data:
        Course.objects.update_or_create(id=course_id, defaults={'name': course_name})

    faculties_data = [
        (1, 'Экономический'),
        (2, 'Юридический'),
    ]
    
    for faculty_id, faculty_name in faculties_data:
        Faculty.objects.update_or_create(id=faculty_id, defaults={'name': faculty_name})

    if not User.objects.filter(username='admin1').exists():
        User.objects.create(
            username='admin1',
            password=make_password('111111Aa_'),
            role=Role.objects.get(id=2),
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
    if not User.objects.filter(username='admin1').exists():
        User.objects.create(
            username='dean',
            password=make_password('111111Aa_'),
            role=Role.objects.get(id=4),
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
    if not User.objects.filter(username='admin2').exists():
        User.objects.create(
            username='admin2',
            password=make_password('111111Aa_'),
            role=Role.objects.get(id=3),
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_roles_and_users),
    ]
