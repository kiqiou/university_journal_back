# Generated by Django 5.2.4 on 2025-07-15 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_user_groups_user_is_active_user_is_staff_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subgroup',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
