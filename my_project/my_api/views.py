from django.core.serializers import serialize
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from selenium.webdriver.common.devtools.v85.layer_tree import LayerId

from .models import MyUser
from .serializer import MyUserSerializer

@api_view(['GET']) #what type of request is made
def get_all_users(request):
    users = MyUser.objects.all()
    serializer = MyUserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
    serializer = MyUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, user_id):
    try:
        user = MyUser.objects.get(id=user_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MyUserSerializer(user)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = MyUserSerializer(user, data=request.data)
        if serializer.is_valid():
            # updates the database
            serializer.save()
            return Response(serializer.data)

    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


