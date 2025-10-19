from django.urls import path

from authentication.views.group_views.group import add_group, delete_group, get_groups_list, get_groups_simple_list, update_group

urlpatterns = [
    path('api/get_groups_simple_list/', get_groups_simple_list),
    path('api/get_groups_list/', get_groups_list),
    path('api/add_group/', add_group),
    path('api/delete_group/', delete_group),
    path('api/update_group/', update_group),
]
