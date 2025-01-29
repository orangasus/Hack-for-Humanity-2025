from django.urls import path
from .views import check_review_for_nsfw

# Define URL patterns for the review views
urlpatterns = [
    # URL pattern for listing the latest reviews
    path('test_ai_mod/', check_review_for_nsfw, name='check_ai_mod'),
]