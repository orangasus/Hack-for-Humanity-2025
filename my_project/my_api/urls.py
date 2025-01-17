from django.urls import path
from .views import create_user, get_all_users, user_detail

urlpatterns = [
    path('users/get_all_users', get_all_users, name='get_all_users'),
    path('users/create_user', create_user, name='create_user'),
    path('users/<int:user_id>', user_detail, name='user_detail')
]