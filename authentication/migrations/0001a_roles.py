from django.db import migrations

def create_roles(apps, schema_editor):
    Role = apps.get_model('authentication', 'Role')

    roles = [
        (1, "Преподаватель"),
        (2, "Администратор 1"),
        (3, "Администратор 2"),
        (4, "Декан"),
        (5, "Студент"),
    ]

    for role_id, name in roles:
        Role.objects.update_or_create(
            id=role_id,
            defaults={"role": name}
        )

class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_roles),
    ]
