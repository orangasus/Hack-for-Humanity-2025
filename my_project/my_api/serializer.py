from rest_framework import serializers
from .models import MyUser

# how models transform into json
class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'