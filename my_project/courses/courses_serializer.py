from rest_framework import serializers
from .models import Course

# how models transform into json
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'