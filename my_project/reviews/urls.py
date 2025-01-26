from django.urls import path
from .views import LatestReviewsView, ReviewCreateView, ReviewDetailView

# Define URL patterns for the review views
urlpatterns = [
    # URL pattern for listing the latest reviews
    path('latest_reviews/', LatestReviewsView.as_view(), name='latest_reviews'),
    # URL pattern for creating a new review
    path('create/', ReviewCreateView.as_view(), name='review_create'),
    # URL pattern for retrieving, updating, or deleting a review by ID
    path('<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
]