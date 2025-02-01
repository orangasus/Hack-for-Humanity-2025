from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .courses_serializer import CourseSerializer, CourseRatingSerializer
from .custom_responses import (
    COURSE_RETRIEVED_RESPONSE, COURSE_NOT_FOUND_RESPONSE, COURSE_CREATED_RESPONSE,
    COURSE_CREATION_ERROR, COURSE_UPDATED_RESPONSE, COURSE_UPDATE_ERROR,
    COURSE_DELETED_RESPONSE, COURSE_DELETION_ERROR, COURSE_LIST_RESPONSE,
    COURSE_SEARCH_RESPONSE, COURSE_RATING_UPDATED_RESPONSE, COURSE_RATING_UPDATE_ERROR,GET_SESSION_ERROR_RESPONSE
)
from .models import Course, CourseStatus

"""
Views responsible for operations with Course model
"""
def check_login_status(request):
    value = request.session.get('user.id', 'default_value')
    if value == 'default_value':
        return False
    return True
    #insert this if in any needed function where the user must be logged in to access
    #if not check_login_status(request):
        #return Response(GET_SESSION_ERROR_RESPONSE("not logged in"), status=status.HTTP_401_UNAUTHORIZED)
    #add this if needed in a class request = self.request

# Helper function to check if user is an admin
def is_admin(user):
    return user.is_staff or user.is_superuser


def get_profs_names_for_course(course):
    return [prof.full_name for prof in course.professors.all()]


def get_uni_name_for_course(course):
    return course.university.uni_name


@api_view(['GET'])
def get_course_by_id(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except:
        return Response(COURSE_NOT_FOUND_RESPONSE, status=status.HTTP_404_NOT_FOUND)
    else:
        profs = get_profs_names_for_course(course)
        uni = get_uni_name_for_course(course)

        serializer = CourseSerializer(course)
        return Response(COURSE_RETRIEVED_RESPONSE(serializer.data, profs, uni), status=status.HTTP_200_OK)


@api_view(['POST'])
# admin check
def create_course(request):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        try:
            professors_data = request.data.get('professors', [])
            if not isinstance(professors_data, list):
                return Response({'error': 'Professors data should be a list.'}, status=status.HTTP_400_BAD_REQUEST)

            course = serializer.save()  # Save the Course instance to get the primary key
            course.professors.set(professors_data)  # Set the list of professors
            course.save()

            return Response({'message': 'Course created successfully!', 'course': serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseSearchView(generics.ListAPIView):
    serializer_class = CourseSerializer

    # Override the get_queryset method to filter courses based on Course Name or Course Code
    def get_queryset(self):
        query = self.request.query_params.get('search_query', '')
        return Course.objects.filter(
            Q(course_name__icontains=query) |
            Q(course_code__icontains=query)
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(COURSE_SEARCH_RESPONSE(response.data), status=status.HTTP_200_OK)


class CourseRatingView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseRatingSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        # Update the ratings of professors teaching this course
        for professor in instance.professors.all():
            professor.update_rating()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response(COURSE_RATING_UPDATED_RESPONSE, status=status.HTTP_200_OK)
        return Response(COURSE_RATING_UPDATE_ERROR(response.data), status=response.status_code)


# View to search for courses within a specific university

class CourseSearchView_Uni(generics.ListAPIView):
    serializer_class = CourseSerializer

    # Override the get_queryset method to filter courses based on university ID and search query=course_name
    def get_queryset(self):
        university_id = self.kwargs['uni_id']
        query = self.request.query_params.get('search_query', '')
        return Course.objects.filter(university_id=university_id, course_name__icontains=query)


@api_view(['PUT'])
@user_passes_test(is_admin)
def update_course_by_id(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except:
        return Response(COURSE_NOT_FOUND_RESPONSE, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = CourseSerializer(course, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(COURSE_UPDATED_RESPONSE(serializer.data), status=status.HTTP_200_OK)
        return Response(COURSE_UPDATE_ERROR(serializer.errors), status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@user_passes_test(is_admin)
def delete_course_by_id(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except:
        return Response(COURSE_NOT_FOUND_RESPONSE, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            course.delete()
            return Response(COURSE_DELETED_RESPONSE, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(COURSE_DELETION_ERROR(str(e)), status=status.HTTP_400_BAD_REQUEST)


class Course_Status_Update_View(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def update(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])
        new_status = request.data.get('course_status')
        if int(new_status) not in [status.value for status in CourseStatus]:  # Ensure proper type conversion
            return Response({"error": "Invalid status value."}, status=status.HTTP_400_BAD_REQUEST)

        course.course_status = int(new_status)  # Ensure proper type conversion
        course.save()
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class Course_Status_List_View(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        status = self.request.query_params.get('course_status')
        if status and status.isdigit() and int(status) in [status.value for status in CourseStatus]:
            return Course.objects.filter(course_status=int(status))
        return

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(COURSE_LIST_RESPONSE(serializer.data), status=status.HTTP_200_OK)


class Get_All_Courses(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)