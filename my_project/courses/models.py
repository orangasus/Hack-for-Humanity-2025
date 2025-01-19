from enum import IntEnum

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

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
    course_rating = models.IntegerField(
        validators=[MinValueValidator(MIN_COURSE_RATING), MaxValueValidator(MAX_COURSE_RATING)], default=MIN_COURSE_RATING)
    review_status = models.IntegerField(choices=CourseStatus.choices(), default=CourseStatus.UNDER_REVIEW)

    university = models.ForeignKey('uni_prof.University', name='courses', on_delete=models.CASCADE)
    professor = models.ManyToManyField('uni_prof.Professor', name='professors')
