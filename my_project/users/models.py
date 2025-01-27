from django.db import models
from django.contrib.auth.models import User
from .utils import animal_names, adjectives
from random import randint


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    public_username = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return str(self.user)

    def generate_public_name(self):
        animal_len = len(animal_names)
        adj_len = len(adjectives)
        animal = animal_names[randint(0, animal_len-1)]
        adj = adjectives[randint(0, adj_len-1)]
        self.public_username = f'{adj}-{animal}-{self.user.id}'
        self.save()