from enum import IntEnum

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

    departments = models.JSONField()

    date_added = models.DateField(auto_now_add=True)
    date_last_modified = models.DateField(auto_now=True)

    course_status = models.IntegerField(choices=CourseStatus.choices(), default=CourseStatus.UNDER_REVIEW)

    avg_course_rating = models.DecimalField(decimal_places=1, max_digits=2, blank=True, null=True)

    avg_cognitive_load_rating = models.DecimalField(decimal_places=1, max_digits=2, blank=True, null=True)
    avg_delivery_support_rating = models.DecimalField(decimal_places=1, max_digits=2, blank=True, null=True)
    avg_engagement_enjoyment_rating = models.DecimalField(decimal_places=1, max_digits=2, blank=True, null=True)
    avg_usefulness_relevance_rating = models.DecimalField(decimal_places=1, max_digits=2, blank=True, null=True)

    university = models.ForeignKey('uni_prof.University', related_name='courses', on_delete=models.CASCADE)
    professors = models.ManyToManyField('uni_prof.Professor', related_name='courses')

    def update_rating(self):
        avg_rating = self.reviews.aggregate(Avg('overall_rating'))['overall_rating__avg']
        avg_cog_load = self.reviews.aggregate(Avg('cognitive_load_rating'))['cognitive_load_rating__avg']
        avg_delivery_support = self.reviews.aggregate(Avg('delivery_support_rating'))['delivery_support_rating__avg']
        avg_engagement_enjoyment = self.reviews.aggregate(Avg('engagement_enjoyment_rating'))[
            'engagement_enjoyment_rating__avg']
        avg_usefulness_relevance = self.reviews.aggregate(Avg('usefulness_relevance_rating'))[
            'usefulness_relevance_rating__avg']

        self.avg_course_rating = avg_rating or MIN_COURSE_RATING

        self.avg_cognitive_load_rating = round(avg_cog_load, 1) or MIN_COURSE_RATING
        self.avg_delivery_support_rating = round(avg_delivery_support, 1) or MIN_COURSE_RATING
        self.avg_engagement_enjoyment_rating = round(avg_engagement_enjoyment, 1) or MIN_COURSE_RATING
        self.avg_usefulness_relevance_rating = round(avg_usefulness_relevance, 1) or MIN_COURSE_RATING

        self.save()
