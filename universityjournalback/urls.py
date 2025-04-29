from django.urls import include, path
from .views import get_attendance

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('api/attendance/', get_attendance, name = 'attendance')
]


