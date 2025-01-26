from rest_framework import generics
from .models import University, Professor
from .serializers import UniversitySerializer, ProfessorRatingSerializer, ProfessorSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
# Helper function to check if user is an admin
def is_admin(user):
    return user.is_staff or user.is_superuser

# View for searching universities
class UniversitySearchView(generics.ListAPIView):
    serializer_class = UniversitySerializer

    # Override the get_queryset method to filter universities based on search query
    def get_queryset(self):
        query = self.request.query_params.get('search_query', '')
        return University.objects.filter(title__icontains=query)

# View for updating professor ratings
class ProfessorRatingView(generics.UpdateAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorRatingSerializer

# API view for creating a university
@api_view(['POST'])
@login_required
@user_passes_test(is_admin)
def create_university(request):
    serializer = UniversitySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API view for creating a professor
@api_view(['POST'])
@login_required
@user_passes_test(is_admin)
def create_professor(request):
    serializer = ProfessorSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API view for getting all professors
@api_view(['GET'])
def get_all_professors(request):
    users = Professor.objects.all()
    serializer = ProfessorSerializer(users, many=True)
    return Response(serializer.data)