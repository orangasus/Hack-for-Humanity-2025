from django.urls import path
from .views import LatestReviewsView, ReviewCreateView, ReviewDetailView,Reviews_Status_Update_View,Reviews_Status_List_View,Get_All_Reviews

# Define URL patterns for the review views
urlpatterns = [
    # URL pattern for listing the latest reviews
    path('latest_reviews/', LatestReviewsView.as_view(), name='latest_reviews'),
    # URL pattern for creating a new review
    path('create/', ReviewCreateView.as_view(), name='review_create'),
    # URL pattern for retrieving, updating, or deleting a review by ID
    path('<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),

    path('review/<int:pk>/status/', Reviews_Status_Update_View.as_view(), name='Review_status_update'),#http://127.0.0.1:8000/reviews/review/1/status/
    path('status/', Reviews_Status_List_View.as_view(), name='Review_status_list'),#/reviews/status/?review_status=<status_value>
    path('get_all_reviews/', Get_All_Reviews.as_view(), name='get_all_reviews'),
    

]