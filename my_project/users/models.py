from django.db import models
from django.contrib.auth.models import User

class ExtendedUser(models.Model):
    # associate with default user model
    # with one-to-one field associations
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    public_username = models.CharField(max_length=20)

    def __str__(self):
        return str(self.user)