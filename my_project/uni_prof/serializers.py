from rest_framework import serializers
from .models import University,Professor

# how models transform into json
class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'
class ProfessorRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['id', 'rating']