from django.db import models

class MyUser(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return f"""
        Username: {self.username}
        Password: {self.password}"""
