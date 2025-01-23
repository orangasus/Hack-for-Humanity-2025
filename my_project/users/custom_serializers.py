from django.contrib.auth.models import User
from rest_framework import serializers

from .models import ExtendedUser


# how models transform into json
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class ExtendedUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ExtendedUser
        fields = ('id', 'public_username', 'user')
