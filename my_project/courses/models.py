from enum import IntEnum

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg

MAX_COURSE_RATING = 5
MIN_COURSE_RATING = 1


class CourseStatus(IntEnum):
    OK = 1
    UNDER_REVIEW = 2
    ARCHIVED = 3
    DELETED = 4

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=30)
    date_added = models.DateField(auto_now_add=True)
    date_last_modified = models.DateField(auto_now=True)
    course_rating = models.FloatField(
        validators=[MinValueValidator(MIN_COURSE_RATING), MaxValueValidator(MAX_COURSE_RATING)], default=MIN_COURSE_RATING)
    course_status = models.IntegerField(choices=CourseStatus.choices(), default=CourseStatus.UNDER_REVIEW)

    university = models.ForeignKey('uni_prof.University', related_name='courses', on_delete=models.CASCADE)
    professors = models.ManyToManyField('uni_prof.Professor', related_name='courses')

    def update_rating(self):
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        self.course_rating = avg_rating if avg_rating is not None else MIN_COURSE_RATING
        self.save()