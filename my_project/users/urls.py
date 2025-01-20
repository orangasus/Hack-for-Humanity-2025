from django.urls import path
from .views import get_all_users, create_user, delete_user_by_id, update_user_by_id, get_user_by_id, login_user, logout_user, signup_user,set_session,get_session,delete_session,send_test_email

urlpatterns = [
    path('get_all_users', get_all_users, name='get_all_users'),
    path('create_user', create_user, name='create_user'),
    path('delete_user/<int:user_id>', delete_user_by_id, name='delete_user'),
    path('update_user/<int:user_id>', update_user_by_id, name='update_user'),
    path('get_user/<int:user_id>', get_user_by_id, name='get_user'),
    path('login', login_user, name='login_user'),
    path('logout', logout_user, name='logout_user'),
    path('signup', signup_user, name='signup_user'),
    path('set_session/', set_session, name='set_session'),
    path('get_session/', get_session, name='get_session'),
    path('delete_session/', delete_session, name='delete_session'),
    path('send_test_email/', send_test_email, name='send_test_email'),
]