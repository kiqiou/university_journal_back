from django.urls import include, path
from .views import delete_course, get_attendance, add_session, delete_session, get_groups_list
from .views import get_teacher_list, delete_user, update_user, update_attendance, update_session, get_courses_list,add_or_update_course

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
    path('api/add_or_update_course/', add_or_update_course),
    path('api/delete_course/', delete_course),
    path('api/get_groups_list', get_groups_list)
]