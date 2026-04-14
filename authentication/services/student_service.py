from attestation.models import Attestation
from authentication.models.user import StudentProfile
from journal.models.session import Attendance, Session
from journal.models.discipline import Discipline
def initialize_student_data(student_profile):
    group = student_profile.group
    user = student_profile.user

    # 1. Распределение подгрупп для ВСЕХ студентов группы
    all_students = StudentProfile.objects.filter(group=group).order_by('user__username')
    unassigned_students = [s for s in all_students if not s.subGroup]
    half = len(unassigned_students) // 2
    for i, s in enumerate(unassigned_students):
        s.subGroup = 1 if i < half else 2
        s.save()

    # 2. Disciplines группы
    disciplines = Discipline.objects.filter(groups=group)

    # 3. Attestations для этого студента (по всем дисциплинам группы)
    for discipline in disciplines:
        Attestation.objects.get_or_create(
            student=user,
            group=group,
            discipline=discipline,
            defaults={'result': ''}
        )

    # 4. Sessions ЭТОЙ группы по этим дисциплинам (КРИТИЧНО: + group=group)
    sessions = Session.objects.filter(
        course__in=disciplines,
        group=group  # Добавьте это!
    )
    
    # Bulk create attendances (как в старом коде, эффективно)
    attendances = [
        Attendance(
            session=session, 
            student=user, 
            status=' ',  # 'Присутствовал' по умолчанию
            grade=None
        )
        for session in sessions
    ]
    Attendance.objects.bulk_create(attendances, ignore_conflicts=True)