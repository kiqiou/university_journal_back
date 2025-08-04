from django.urls import path

from attestation.views import add_usr, delete_usr, get_attestation, update_usr

urlpatterns = [
    path('api/get_attestation/', get_attestation),
    path('api/add_usr/',  add_usr),
    path('api/update_usr/', update_usr),
    path('api/delete_course/', delete_usr),
]
