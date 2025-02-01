from idlelib.iomenu import errors

from rest_framework import generics
from .models import University, Professor
from .serializers import UniversitySerializer, ProfessorRatingSerializer, ProfessorSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import  user_passes_test
from .custom_responses import (
    UNIVERSITY_CREATED_RESPONSE, UNIVERSITY_CREATION_ERROR,
    PROFESSOR_CREATED_RESPONSE, PROFESSOR_CREATION_ERROR,
    PROFESSOR_RATING_UPDATED_RESPONSE, PROFESSOR_RATING_UPDATE_ERROR, UNI_INFO_BY_ID_RESPONSE,GET_SESSION_ERROR_RESPONSE
)
from courses.courses_serializer import CourseSerializer


# Create your views here.
# Helper function to check if user is an admin
def is_admin(user):
    return user.is_staff or user.is_superuser

def check_login_status(request):
    value = request.session.get('user.id', 'default_value')
    if value == 'default_value':
        return False
    return True
    #insert this if in any needed function where the user must be logged in to access
    #if not check_login_status(request):
        #return Response(GET_SESSION_ERROR_RESPONSE("not logged in"), status=status.HTTP_401_UNAUTHORIZED)
        #add this if needed in a class request = self.request 

@api_view(['GET'])
def get_uni_info_by_id(request, uni_id):
    uni = University.objects.get(id=uni_id)
    profs = uni.professors.all()
    courses = uni.courses.all()

    uni_serializer = UniversitySerializer(uni)
    profs_serializer = ProfessorSerializer(profs, many=True)
    courses_serializer = CourseSerializer(courses, many=True)

    return Response(UNI_INFO_BY_ID_RESPONSE(uni_serializer.data,
                                            profs_serializer.data, courses_serializer.data),
                    status=status.HTTP_200_OK)

@api_view(['GET'])
def search_profs_by_name(request):
    query = request.GET.get('query')
    print(query)
    if query:
        profs = Professor.objects.filter(full_name__icontains=query)
    else:
        profs = Professor.objects.all()
    serializer = ProfessorSerializer(profs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# View for searching universities
class UniversitySearchView(generics.ListAPIView):
    serializer_class = UniversitySerializer

    # Override the get_queryset method to filter universities based on search query
    def get_queryset(self):
        query = self.request.query_params.get('search_query', '')
        return University.objects.filter(uni_name__icontains=query)


# View for updating professor ratings
class ProfessorRatingView(generics.UpdateAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorRatingSerializer

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response(PROFESSOR_RATING_UPDATED_RESPONSE, status=status.HTTP_200_OK)
        return Response(PROFESSOR_RATING_UPDATE_ERROR(response.data), status=response.status_code)

# API view for creating a university
@api_view(['POST'])
# @user_passes_test(is_admin)
def create_university(request):
    serializer = UniversitySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(UNIVERSITY_CREATED_RESPONSE(serializer.data), status=status.HTTP_201_CREATED)
    return Response(UNIVERSITY_CREATION_ERROR(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_prof_name_rating_by_id(request, prof_id):
    try:
        prof = Professor.objects.get(id=prof_id)
        name = prof.full_name
        rating = prof.rating
        return Response({"name":name, "rating": rating}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# API view for creating a professor
@api_view(['POST'])
# @user_passes_test(is_admin)
def create_professor(request):
    serializer = ProfessorSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(PROFESSOR_CREATED_RESPONSE(serializer.data), status=status.HTTP_201_CREATED)
    return Response(PROFESSOR_CREATION_ERROR(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

# API view for getting all professors
@api_view(['GET'])
def get_all_professors(request):
    users = Professor.objects.all()
    serializer = ProfessorSerializer(users, many=True)
    return Response(serializer.data)