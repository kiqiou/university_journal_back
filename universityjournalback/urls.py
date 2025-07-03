from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import add_discipline, add_group, delete_course, delete_group, get_attendance, add_session, delete_session, get_groups_list, get_student_list, get_students_by_group, update_discipline, update_group
from .views import get_teacher_list, delete_user, update_user, update_attendance, update_session, get_courses_list, update_teacher_disciplines

urlpatterns = [
    path('auth/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('authentication.urls')),
    path('api/get_attendance/', get_attendance),
    path('api/update_attendance/', update_attendance),
    path('api/update_session/<int:id>/', update_session),
    path('api/add_session/', add_session),
    path('api/delete_session/', delete_session),
    path('api/get_teacher_list/', get_teacher_list),
    path('api/get_student_list/', get_student_list),
    path('api/get_students_by_group/', get_students_by_group),
    path('api/update_user/<int:user_id>/', update_user,),
    path('api/update_teacher_disciplines/', update_teacher_disciplines),
    path('api/delete_user/', delete_user),
    path('api/get_courses_list/', get_courses_list),
    path('api/add_course/', add_discipline),
    path('api/update_course/', update_discipline),
    path('api/delete_course/', delete_course),
    path('api/get_groups_list/', get_groups_list),
    path('api/add_group/', add_group),
    path('api/delete_group/', delete_group),
    path('api/update_group/', update_group),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)