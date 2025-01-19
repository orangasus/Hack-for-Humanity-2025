from django.db import models

class University(models.Model):
    uni_name = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)

    professors = models.ManyToManyField('uni_prof.Professor', related_name='professors')


class Professor(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    date_added = models.DateField(auto_now_add=True)

    courses = models.ManyToManyField('courses.Course', null=True)
    universities = models.ManyToManyField('uni_prof.University')
