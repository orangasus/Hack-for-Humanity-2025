from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .courses_serializer import CourseSerializer
from .models import Course

"""
Views responsible for operations with Course model
"""


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
def create_course(request):
    serializer = CourseSerializer(request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
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
