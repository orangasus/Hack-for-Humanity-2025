from django.contrib.auth import authenticate, logout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .extended_user_serializer import ExtendedUserSerializer
from .models import ExtendedUser


@api_view(['GET'])
def get_all_users(request):
    users = ExtendedUser.objects.all()
    serializer = ExtendedUserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_user(request):
    serializer = ExtendedUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user_by_id(request, user_id):
    try:
        user_to_delete = ExtendedUser.objects.get(id=user_id)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        user_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def update_user_by_id(request, user_id):
    try:
        user_to_update = ExtendedUser.objects.get(id=user_id)
        serializer = ExtendedUserSerializer(user_to_update, data=request.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_by_id(request, user_id):
    try:
        user_to_get = ExtendedUser.objects.get(id=user_id)
        serializer = ExtendedUserSerializer(user_to_get)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)
    if user:
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def signup_user(request):
    # some checks e.g. if username exists
    create_user(request)

@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)
