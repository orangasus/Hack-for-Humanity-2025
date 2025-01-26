from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .courses_serializer import CourseSerializer
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

"""
Views responsible for operations with Course model
"""
# Helper function to check if user is an admin
def is_admin(user):
    return user.is_staff or user.is_superuser


@api_view(['GET'])
def get_course_by_id(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@login_required
@user_passes_test(is_admin)
def create_course(request):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseSearchView(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        university_id = self.kwargs['uni_id']
        query = self.request.query_params.get('search_query', '')
        return Course.objects.filter(university_id=university_id, course_name__icontains=query)

class CourseRatingView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseRatingSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        # Update the ratings of professors teaching this course
        for professor in instance.professors.all():
            professor.update_rating()

@api_view(['PUT'])
@login_required
@user_passes_test(is_admin)
def update_course_by_id(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = CourseSerializer(course, request.data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@login_required
@user_passes_test(is_admin)
def delete_course_by_id(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        course.delete()
        return Response(status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_all_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

