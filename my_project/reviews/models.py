from enum import IntEnum

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from my_project.metrics_related import MetricsWeights

MAX_COURSE_RATING=5
MIN_COURSE_RATING=1

class ReviewStatus(IntEnum):
    PASSED_REVIEW = 1
    UNDER_REVIEW = 2
    FAILED_REVIEW = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Review(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    review_status = models.IntegerField(choices=ReviewStatus.choices(), default=ReviewStatus.UNDER_REVIEW)

    cognitive_load_rating = models.IntegerField(
        validators=[MinValueValidator(MIN_COURSE_RATING), MaxValueValidator(MAX_COURSE_RATING)], default=MIN_COURSE_RATING)
    delivery_support_rating = models.IntegerField(
        validators=[MinValueValidator(MIN_COURSE_RATING), MaxValueValidator(MAX_COURSE_RATING)], default=MIN_COURSE_RATING)
    engagement_enjoyment_rating = models.IntegerField(
        validators=[MinValueValidator(MIN_COURSE_RATING), MaxValueValidator(MAX_COURSE_RATING)], default=MIN_COURSE_RATING)
    usefulness_relevance_rating = models.IntegerField(
        validators=[MinValueValidator(MIN_COURSE_RATING), MaxValueValidator(MAX_COURSE_RATING)], default=MIN_COURSE_RATING)

    overall_rating = models.DecimalField(decimal_places=1, max_digits=2, blank=True)

    user = models.ForeignKey('users.ExtendedUser', related_name='reviews', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', related_name='reviews', on_delete=models.DO_NOTHING)

    def calculate_overall_rating(self):
        overall_rating = (MetricsWeights.COGNITIVE_LOAD * self.cognitive_load_rating +
                          MetricsWeights.DELIVERY_SUPPORT * self.delivery_support_rating +
                          MetricsWeights.ENGAGEMENT_ENJOYMENT * self.engagement_enjoyment_rating +
                          MetricsWeights.USEFULNESS_RELEVANCE * self.usefulness_relevance_rating) / 100
        self.overall_rating = round(overall_rating, 1)

    def save(self, *args, **kwargs):
        self.calculate_overall_rating()
        super().save(*args, **kwargs)

