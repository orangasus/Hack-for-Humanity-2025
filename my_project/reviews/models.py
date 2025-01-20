from enum import IntEnum

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

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
    rating_left = models.IntegerField(
        validators=[MinValueValidator(MIN_COURSE_RATING), MaxValueValidator(MAX_COURSE_RATING)], default=MIN_COURSE_RATING)
    date_created = models.DateField(auto_now_add=True)
    review_status = models.IntegerField(choices=ReviewStatus.choices(), default=ReviewStatus.UNDER_REVIEW)

    user = models.ForeignKey('users.ExtendedUser', name='author', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', name='course_reviewed', on_delete=models.DO_NOTHING)
