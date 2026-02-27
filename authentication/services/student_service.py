from attestation.models import Attestation
from journal.models.session import Attendance, Session
from journal.models.discipline import Discipline

def initialize_student_data(student_profile):
    group = student_profile.group
    user = student_profile.user

    all_students = student_profile.__class__.objects.filter(group=group).order_by('user__username')

    unassigned_students = [s for s in all_students if not s.subGroup]
    half = len(unassigned_students) // 2
    for i, s in enumerate(unassigned_students):
        s.subGroup = 1 if i < half else 2
        s.save()

    disciplines = Discipline.objects.filter(groups=group)
    for discipline in disciplines:
        Attestation.objects.get_or_create(
            student=user,
            group=group,
            discipline=discipline,
            defaults={'result': ''}
        )

    sessions = Session.objects.filter(course__in=disciplines)
    for session in sessions:
        Attendance.objects.get_or_create(
            session=session,
            student=user,
            defaults={'status': '', 'grade': None}
        )

