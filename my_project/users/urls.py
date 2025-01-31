from django.urls import path

from .views import (get_all_users, delete_user_by_id, update_user_by_id,
                    get_user_by_id, login_user, logout_user, signup_user, set_session, get_session, delete_session,
                    password_reset_check_token, reset_user_password, reset_password_request,get_session_username)

urlpatterns = [
    # URL pattern for getting all users
    path('get_all_users', get_all_users, name='get_all_users'),
    # URL pattern for deleting a user by ID
    path('delete_user/<int:user_id>', delete_user_by_id, name='delete_user'),
    # URL pattern for updating a user by ID
    path('update_user/<int:user_id>', update_user_by_id, name='update_user'),
    # URL pattern for getting a user by ID
    path('get_user/<int:user_id>', get_user_by_id, name='get_user'),

    # URL pattern for user login
    path('login', login_user, name='login_user'),
    # URL pattern for user logout
    path('logout', logout_user, name='logout_user'),
    # URL pattern for user signup
    path('signup', signup_user, name='signup_user'),

    # URL pattern for setting a session variable
    path('set_session/', set_session, name='set_session'),
    # URL pattern for getting a session variable
    path('get_session/', get_session, name='get_session'),
     # URL pattern for getting a session variable
    path('get_session/', get_session_username, name='get_session'),
    # URL pattern for deleting a session variable
    path('delete_session/', delete_session, name='delete_session'),

    path('reset_password/<uidb64>/<token>', password_reset_check_token, name='password_reset_check_token'),
    path('reset_password/<int:ex_user_id>/<new_password>', reset_user_password, name='reset_user_password'),
    path('reset_password_request/<int:ex_user_id>', reset_password_request, name='reset_password_request'),
]
