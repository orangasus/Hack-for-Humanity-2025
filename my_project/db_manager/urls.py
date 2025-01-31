from django.urls import path
from .views import delete_all_extended_users, delete_all_courses, delete_all_reviews, delete_all_profs, delete_all_unis, flush_db

urlpatterns = [
    path('delete_all_extended_users/', delete_all_extended_users, name='delete_all_extended_users'),
    path('delete_all_courses/', delete_all_courses, name='delete_all_courses'),
    path('delete_all_reviews/', delete_all_reviews, name='delete_all_reviews'),
    path('delete_all_profs/', delete_all_profs, name='delete_all_profs'),
    path('delete_all_unis/', delete_all_unis, name='delete_all_unis'),
    path('flush_db/', flush_db, name='flush_db'),
]
