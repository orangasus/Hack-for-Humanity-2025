from rest_framework import serializers
from .models import Course

from django.core.validators import MinValueValidator, MaxValueValidator

# how models transform into json
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CourseRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_rating']
        extra_kwargs = {
            'course_rating': {
                'validators': [
                    MinValueValidator(1),
                    MaxValueValidator(5)
                ]
            }
        }