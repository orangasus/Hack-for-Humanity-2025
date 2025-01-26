from django.db import models


class University(models.Model):
    uni_name = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)


class Professor(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    date_added = models.DateField(auto_now_add=True)

    universities = models.ManyToManyField('uni_prof.University', related_name='professors')
