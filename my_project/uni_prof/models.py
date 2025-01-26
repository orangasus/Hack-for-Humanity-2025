from django.db import models
from django.db.models import Avg

class University(models.Model):
    uni_name = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)


class Professor(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    date_added = models.DateField(auto_now_add=True)

    universities = models.ManyToManyField('uni_prof.University', related_name='professors')

    def update_rating(self):
        if self.courses.exists():
            avg_rating = self.courses.aggregate(Avg('course_rating'))['course_rating__avg']
            self.rating = avg_rating if avg_rating is not None else 0
            self