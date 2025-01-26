from django.shortcuts import render
from rest_framework import generics
from .models import Review
from .serializers import ReviewSerializer
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
# View to list the latest reviews
class LatestReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    # Override the get_queryset method to return the latest 'n' reviews
    def get_queryset(self):
        n = int(self.request.query_params.get('n', 5))
        return Review.objects.order_by('-created_at')[:n]

# View to create a new review
@login_required
class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # Override the perform_create method to update the course rating after creating a review
    def perform_create(self, serializer):
        instance = serializer.save()
        instance.course.update_rating()

# View to retrieve, update, or delete a review
@login_required
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # Override the perform_update method to update the course rating after updating a review
    def perform_update(self, serializer):
        instance = serializer.save()
        instance.course.update_rating()

    # Override the perform_destroy method to update the course rating after deleting a review
    def perform_destroy(self, instance):
        course = instance.course
        instance.delete()
        course.update_rating()