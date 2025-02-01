from django.contrib.auth.decorators import user_passes_test
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from users.models import ExtendedUser
from courses.models import Course
from reviews.models import Review
from uni_prof.models import University, Professor
from .custom_responses import *

def is_admin(user):
    return user.is_staff or user.is_superuser


@api_view(['DELETE'])
def delete_all_extended_users(request):
    user = request.user
    if not is_admin(user):
      return Response(GET_SESSION_ERROR_RESPONSE("not logged in"), status=status.HTTP_401_UNAUTHORIZED)
    try:
        ExtendedUser.objects.all().delete()
        return Response("All ExtendedUser instances deleted successfully.", status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_all_courses(request):
    user = request.user
    if not is_admin(user):
      return Response(GET_SESSION_ERROR_RESPONSE("not logged in"), status=status.HTTP_401_UNAUTHORIZED)
    try:
        Course.objects.all().delete()
        return Response("All Course instances deleted successfully.", status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_all_reviews(request):
    user = request.user
    if not is_admin(user):
      return Response(GET_SESSION_ERROR_RESPONSE("not logged in"), status=status.HTTP_401_UNAUTHORIZED)
    try:
        Review.objects.all().delete()
        return Response("All Review instances deleted successfully.", status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_all_profs(request):
    user = request.user
    if not is_admin(user):
      return Response(GET_SESSION_ERROR_RESPONSE("not logged in"), status=status.HTTP_401_UNAUTHORIZED)
    try:
        Professor.objects.all().delete()
        return Response("All Professor instances deleted successfully.", status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_all_unis(request):
    user = request.user
    if not is_admin(user):
      return Response(GET_SESSION_ERROR_RESPONSE("not logged in"), status=status.HTTP_401_UNAUTHORIZED)
    try:
        University.objects.all().delete()
        return Response("All University instances deleted successfully.", status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def flush_db(request):
    user = request.user
    if not is_admin(user):
      return Response(GET_SESSION_ERROR_RESPONSE("not logged in"), status=status.HTTP_401_UNAUTHORIZED)

    try:
        with transaction.atomic():
            delete_all_extended_users(request)
            delete_all_reviews(request)
            delete_all_courses(request)
            delete_all_profs(request)
            delete_all_unis(request)
        return Response("Database flushed successfully.", status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)