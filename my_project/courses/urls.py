from django.urls import path
from .views import get_all_courses, get_course_by_id, update_course_by_id, delete_course_by_id,create_course

urlpatterns = [
    path('get_course/<int:course_id>', get_course_by_id, name='get_course'),
    path('update_course/<int:course_id>', update_course_by_id, name='update_course'),
    path('delete_course/<int:course_id>', delete_course_by_id, name='delete_course'),
    path('get_all_courses', get_all_courses, name='get_all_courses'),
    path('create_course', create_course, name='create_course'),
]