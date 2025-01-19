from django.urls import path
from .views import get_all_users, create_user, delete_user_by_id, update_user_by_id, get_user_by_id, login_user, \
    logout_user, signup_user

urlpatterns = [
    path('get_all_users', get_all_users, name='get_all_users'),
    path('create_user', create_user, name='create_user'),
    path('delete_user/<int:user_id>', delete_user_by_id, name='delete_user'),
    path('update_user/<int:user_id>', update_user_by_id, name='update_user'),
    path('get_user/<int:user_id>', get_user_by_id, name='get_user'),
    path('login', login_user, name='login_user'),
    path('logout', logout_user, name='logout_user'),
    path('signup', signup_user, name='signup_user')
]