from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_dean_user(apps, schema_editor):
    Role = apps.get_model('authentication', 'Role')
    User = apps.get_model('authentication', 'User')

    # Проверяем, есть ли уже пользователь с логином "dean"
    if not User.objects.filter(username='dean').exists():
        try:
            dean_role = Role.objects.get(id=4)  # id=4 → "Декан"
        except Role.DoesNotExist:
            print("⚠️ Роль 'Декан' (id=4) не найдена. Пользователь не был создан.")
            return

        User.objects.create(
            username='dean',
            password=make_password('111111Aa_'),
            role=dean_role,
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        print("✅ Пользователь 'dean' успешно создан.")
    else:
        print("ℹ️ Пользователь 'dean' уже существует, пропускаем создание.")

class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(create_dean_user),
    ]
