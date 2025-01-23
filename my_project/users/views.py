import logging
from base64 import urlsafe_b64decode

from adodbapi import IntegrityError
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse
from django.utils.encoding import force_str
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from emails.views import send_confirmation_email, send_password_reset_email
from .custom_serializers import ExtendedUserSerializer, UserSerializer
from .models import ExtendedUser
from emails.token_gen import token_generator

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
# @login_required
# @user_passes_test(is_admin)
def get_all_users(request):
    ex_users = ExtendedUser.objects.all()
    serializer = ExtendedUserSerializer(ex_users, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@login_required
@user_passes_test(is_admin)
def delete_user_by_id(request, ex_user_id):
    try:
        user_to_delete = ExtendedUser.objects.get(id=ex_user_id)
        user_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ExtendedUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@login_required
@user_passes_test(is_admin)
def update_user_by_id(request, ex_user_id):
    try:
        user_to_update = ExtendedUser.objects.get(id=ex_user_id)
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
def get_user_by_id(request, ex_user_id):
    try:
        user_to_get = ExtendedUser.objects.get(id=ex_user_id)
        serializer = ExtendedUserSerializer(user_to_get)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ExtendedUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    ex_user = ExtendedUser.objects.get(user=user)
    if user:
        request.session["user.id"] = ex_user.id
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def signup_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    try:
        user = User.objects.create_user(username=username, password=password, email=email)
    except IntegrityError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        user.is_active = False
        user.save()
        ex_user = ExtendedUser.objects.create(user=user, public_username='npc')
        ex_user.save()
        send_confirmation_email(request._request, ex_user)
    return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def reset_password_request(request, ex_user_id):
    ex_user = ExtendedUser.objects.get(id = ex_user_id)
    send_password_reset_email(request, ex_user)
    return HttpResponse('Reset password Email sent!')

@api_view(['GET'])
def password_reset_check_token(request, uidb64, token):
    uid = force_str(urlsafe_b64decode(uidb64))
    ex_user = ExtendedUser.objects.get(pk=uid)

    if token_generator.check_token(ex_user, token):
        # can reset password
        return JsonResponse({'can_reset' : True})
    else:
        # invalid url, can't reset password
        return JsonResponse({'can_reset' : False})

@api_view(['POST'])
def reset_user_password(request, ex_id):
    ex_user = ExtendedUser.objects.get(id=ex_id)
    new_password = request.POST.get('new_password')
    ex_user.user.set_password(new_password)
    ex_user.save()

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
