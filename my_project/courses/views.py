from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.decorators import api_view, permission_classes
import logging
from rest_framework import generics
from .models import Course
from .courses_serializer import CourseSerializer
from .courses_serializer import CourseRatingSerializer
from django.db.models import Q
"""
Views responsible for operations with Course model
"""

# Helper function to check if user is an admin
def is_admin(user):
    return user.is_staff or user.is_superuser

# API view to get a course by ID
@api_view(['GET'])
def get_course_by_id(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CourseSerializer(course)
    return Response(serializer.data, status=status.HTTP_200_OK)

# API view to create a new course
@api_view(['POST'])
#@login_required
#@user_passes_test(is_admin)
def create_course(request):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API view to update a course by ID
@api_view(['PUT'])
@login_required
@user_passes_test(is_admin)
def update_course_by_id(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CourseSerializer(course, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API view to delete a course by ID
@api_view(['DELETE'])
@login_required
@user_passes_test(is_admin)
def delete_course_by_id(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    course.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# API view to get all courses
@api_view(['GET'])
def get_all_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# View to search for courses within a specific university
class CourseSearchView_Uni(generics.ListAPIView):
    serializer_class = CourseSerializer

    # Override the get_queryset method to filter courses based on university ID and search query=course_name
    def get_queryset(self):
        university_id = self.kwargs['uni_id']
        query = self.request.query_params.get('search_query', '')
        return Course.objects.filter(university_id=university_id, course_name__icontains=query)
    
    # View to search for courses within a specific university
class CourseSearchView(generics.ListAPIView):
    serializer_class = CourseSerializer
    # Override the get_queryset method to filter courses based on Course Name or Course Code
    def get_queryset(self):
        query = self.request.query_params.get('search_query', '')
        return Course.objects.filter(
            Q(course_name__icontains=query) | 
            Q(course_code__icontains=query)
        )


# View to update course ratings
class CourseRatingView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseRatingSerializer

    # Override the perform_update method to update professor ratings after updating the course rating
    def perform_update(self, serializer):
        instance = serializer.save()
        for professor in instance.professors.all():
            professor.update_rating()
