from django.urls import path
from .views import UniversitySearchView, ProfessorRatingView, create_professor, create_university, get_all_professors, \
    get_uni_info_by_id, search_profs_by_name

# Define URL patterns for the views
urlpatterns = [
    # URL pattern for university search view
    path('search_query/', UniversitySearchView.as_view(), name='university_search'),
    # URL pattern for professor rating view
    path('<int:pk>/rate/', ProfessorRatingView.as_view(), name='professor_rate'),
    # URL pattern for creating a professor
    path('create_professor', create_professor, name='create_professor'),
    # URL pattern for creating a university
    path('create_university', create_university, name='create_university'),
    # URL pattern for getting all professors
    path('get_all_professors', get_all_professors, name='get_all_professors'),
    path('uni_info_by_id/<int:uni_id>', get_uni_info_by_id, name='get_uni_info_by_id'),
    path('search_professors/', search_profs_by_name, name='search_profs_by_name')
]