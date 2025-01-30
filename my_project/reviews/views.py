from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .custom_responses import (
    LATEST_REVIEWS_RESPONSE, REVIEW_CREATION_ERROR,
    REVIEW_RETRIEVED_RESPONSE, REVIEW_UPDATED_RESPONSE, REVIEW_UPDATE_ERROR,
    REVIEW_DELETED_RESPONSE, REVIEW_DELETION_ERROR, REVIEW_NOT_FOUND_RESPONSE
)
from .models import Review, ReviewStatus
from .serializers import ReviewSerializer


# Create your views here.
# View to list the latest reviews
class LatestReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    # Override the get_queryset method to return the latest 'n' reviews
    def get_queryset(self):
        n = int(self.request.query_params.get('n', 5))
        reviews = Review.objects.order_by('-date_created')[:n]
        return reviews

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(LATEST_REVIEWS_RESPONSE(response.data), status=status.HTTP_200_OK)


# View to create a new review
# @login_required

class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # Override the perform_create method to update the course rating after creating a review
    def perform_create(self, serializer):
        # user = self.request.user
        # course = serializer.validated_data['course']
        # if Review.objects.filter(user=user, course=course).exists():
        #     raise ValidationError("You have already reviewed this course.")

        instance = serializer.save()
        # instance.course.update_rating()

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            if response.status_code == status.HTTP_201_CREATED:
                return Response({"status": "Review created successfully", "data": response.data},
                                status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(REVIEW_CREATION_ERROR(response.data), status=response.status_code)


# View to retrieve, update, or delete a review
# @login_required
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response(REVIEW_RETRIEVED_RESPONSE(response.data), status=status.HTTP_200_OK)
        return Response(REVIEW_NOT_FOUND_RESPONSE, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response(REVIEW_UPDATED_RESPONSE(response.data), status=status.HTTP_200_OK)
        return Response(REVIEW_UPDATE_ERROR(response.data), status=response.status_code)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(REVIEW_DELETED_RESPONSE, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(REVIEW_DELETION_ERROR(str(e)), status=status.HTTP_400_BAD_REQUEST)


class Get_All_Reviews(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_reviews_for_course(request, course_id):
    reviews = Review.objects.filter(course=course_id, review_status=ReviewStatus.PASSED_REVIEW)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class Reviews_Status_Update_View(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def update(self, request, *args, **kwargs):
        review = get_object_or_404(Review, pk=kwargs['pk'])
        new_status = request.data.get('review_status')  # Ensure we're using 'review_status'
        if int(new_status) not in [status.value for status in ReviewStatus]:  # Ensure proper type conversion
            return Response({"error": "Invalid status value."}, status=status.HTTP_400_BAD_REQUEST)

        review.review_status = int(new_status)  # Ensure proper type conversion
        review.save()
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class Reviews_Status_List_View(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        status = self.request.query_params.get('review_status')
        if status and status.isdigit() and int(status) in [status.value for status in ReviewStatus]:
            return Review.objects.filter(review_status=int(status))
        return

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
