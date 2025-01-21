from django.contrib.auth import authenticate, logout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .extended_user_serializer import ExtendedUserSerializer
from .models import ExtendedUser
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
import logging
from django.core.mail import send_mail

# Set up logging
logger = logging.getLogger(__name__)

# Helper function to assign user to a group programmatically
def assign_user_to_group(username, group_name):
    try:
        user = User.objects.get(username=username)
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        logger.info(f"User {username} added to group {group_name}")
    except User.DoesNotExist:
        logger.error(f"User {username} does not exist")
    except Group.DoesNotExist:
        logger.error(f"Group {group_name} does not exist")

# Helper function to check if user is an admin
def is_admin(user):
    return user.is_staff or user.is_superuser

@api_view(['GET'])
@login_required
@user_passes_test(is_admin)
def get_all_users(request):
    users = ExtendedUser.objects.all()
    serializer = ExtendedUserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@login_required
@user_passes_test(is_admin)
def create_user(request):
    serializer = ExtendedUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@login_required
@user_passes_test(is_admin)
def delete_user_by_id(request, user_id):
    try:
        user_to_delete = ExtendedUser.objects.get(id=user_id)
        user_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ExtendedUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@login_required
@user_passes_test(is_admin)
def update_user_by_id(request, user_id):
    try:
        user_to_update = ExtendedUser.objects.get(id=user_id)
    except ExtendedUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ExtendedUserSerializer(user_to_update, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@login_required
@user_passes_test(is_admin)
def get_user_by_id(request, user_id):
    try:
        user_to_get = ExtendedUser.objects.get(id=user_id)
        serializer = ExtendedUserSerializer(user_to_get)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ExtendedUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        request.session["user.id"] = user.id
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def signup_user(request):
    # You may want to add more checks and validations here
    return create_user(request)

@api_view(['POST'])
@login_required
def logout_user(request):
    logout(request)
    delete_session()
    return Response(status=status.HTTP_200_OK)

@login_required
@user_passes_test(is_admin)
def set_session(request):
    request.session['key'] = 'value'
    return HttpResponse('Session data set')

@login_required
@user_passes_test(is_admin)
def get_session(request):
    value = request.session.get('user.id', 'default_value')
    return HttpResponse(f'Session data: {value}')

@login_required
@user_passes_test(is_admin)
def delete_session(request):
    try:
        del request.session['user.id']
    except KeyError:
        pass
    return HttpResponse('Session data cleared')

@login_required
@user_passes_test(is_admin)
def send_test_email(request):
    send_mail(
        'Test Email',
        'This is a test email sent from Django.',
        'forgot.ica@gmail.com',
        ['niklas.marchese.ica@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse('Test email sent')
