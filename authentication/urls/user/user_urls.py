from django.urls import path

from authentication.views.user_views.user import delete_user, get_students_by_group, get_teacher_list, update_teacher_disciplines, update_user

urlpatterns = [
    path('api/get_teacher_list/', get_teacher_list),
    path('api/get_students_by_group/', get_students_by_group),
    path('api/update_user/<int:user_id>/', update_user,),
    path('api/update_teacher_disciplines/', update_teacher_disciplines),
    path('api/delete_user/', delete_user),
]
