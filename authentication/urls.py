from django.urls import path
from .views import register_user, login_user, LogoutView

urlpatterns = [
    path('api/register/', register_user, name='register_user'),
    path('api/login/', login_user, name='login_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
