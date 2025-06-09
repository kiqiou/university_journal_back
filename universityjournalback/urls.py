from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static
from .views import add_course, delete_course, get_attendance, add_session, delete_session, get_groups_list, update_course
from .views import get_teacher_list, delete_user, update_user, update_attendance, update_session, get_courses_list

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('api/attendance/', get_attendance),
    path('api/update_attendance/', update_attendance),
    path('api/update_session/<int:id>/', update_session),
    path('api/add_session/', add_session),
    path('api/delete_session/', delete_session),
    path('api/get_teacher_list/', get_teacher_list),
    path('api/update_user/<int:user_id>/', update_user,),
    path('api/delete_user/', delete_user),
    path('api/get_courses_list/', get_courses_list),
    path('api/add_course/', add_course),
    path('api/update_course/', update_course),
    path('api/delete_course/', delete_course),
    path('api/get_groups_list', get_groups_list)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)