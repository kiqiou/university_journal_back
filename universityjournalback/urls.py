from django.urls import path
from .views import get_first_user

urlpatterns = [
    path('api/user/first/', get_first_user, name='get_first_user'),
]

