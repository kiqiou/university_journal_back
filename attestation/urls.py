from django.urls import path

from attestation.views import add_usr, delete_usr, get_attestation, update_attestation, update_usr

urlpatterns = [
    path('api/get_attestation/', get_attestation),
    path('api/update_attestation/', update_attestation),
    path('api/add_usr/',  add_usr),
    path('api/update_usr/', update_usr),
    path('api/delete_usr/', delete_usr),
]
