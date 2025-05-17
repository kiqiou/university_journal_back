from django.urls import include, path
from .views import get_attendance, add_session, delete_session, get_teacher_list, delete_user

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('api/attendance/', get_attendance),
    path('api/add_session/', add_session),
    path('api/delete_session/', delete_session),
    path('api/get_teacher_list/', get_teacher_list),
    path('api/delete_user/', delete_user),
]