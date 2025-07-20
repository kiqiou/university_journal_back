from django.urls import path

from journal.views.session_views.session_views import add_session, delete_session, get_attendance, update_attendance, update_session

urlpatterns = [
    path('api/get_attendance/', get_attendance),
    path('api/update_attendance/', update_attendance),
    path('api/update_session/<int:id>/', update_session),
    path('api/add_session/', add_session),
    path('api/delete_session/', delete_session),
]

