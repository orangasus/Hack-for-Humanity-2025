from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ExtendedUser

# how models transform into json
class ExtendedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtendedUser
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')