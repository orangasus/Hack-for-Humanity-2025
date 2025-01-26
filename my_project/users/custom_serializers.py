from django.contrib.auth.models import User
from rest_framework import serializers

from .models import ExtendedUser


# how models transform into json
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_active')


class ExtendedUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ExtendedUser
        fields = ('id', 'user', 'public_username')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            # Update the User instance
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
        # Update the ExtendedUser instance
        return super().update(instance, validated_data)

