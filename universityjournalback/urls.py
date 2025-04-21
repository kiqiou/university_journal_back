from django.urls import path
from .views import add_role_to_user
from .views import register_user
from .views import login_user

urlpatterns = [
    path('api/user/<int:user_id>/add_role/', add_role_to_user, name='add_role_to_user'),
    path('api/register/', register_user, name='register_user'),
    path('api/login/', login_user, name='login_user'),
]


