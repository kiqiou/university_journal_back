from django.urls import path

from journal.views.discipline_views.disicipline_views import add_discipline, delete_discipline, get_discipline_list, update_discipline

urlpatterns = [
    path('api/get_disciplines_list/', get_discipline_list),
    path('api/add_course/', add_discipline),
    path('api/update_course/', update_discipline),
    path('api/delete_course/', delete_discipline),
]
