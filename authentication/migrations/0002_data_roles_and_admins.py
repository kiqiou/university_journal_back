from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_roles_and_users(apps, schema_editor):
    Role = apps.get_model('authentication', 'Role')
    User = apps.get_model('authentication', 'User')

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
