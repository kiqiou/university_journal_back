from django.urls import include, path
from .views import get_attendance, add_session, delete_session

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('api/attendance/', get_attendance, name = 'attendance'),
    path('api/add_session/', add_session, name = 'add_session'),
    path('api/delete_session/', delete_session, name = 'delete_session'),
]


