from rest_framework import serializers
from .models import ExtendedUser

# how models transform into json
class ExtendedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtendedUser
        fields = '__all__'