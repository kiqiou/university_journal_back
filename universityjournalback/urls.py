from django.urls import path
from .views import add_role_to_user

urlpatterns = [
    path('api/user/<int:user_id>/add_role/', add_role_to_user, name='add_role_to_user'),
]


