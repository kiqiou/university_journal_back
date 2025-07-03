from django.urls import path
from .views import register_user, LogoutView, user_info

urlpatterns = [
    path('api/register/', register_user, name='register_user'),
    path('api/user/', user_info, name='user_info'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
