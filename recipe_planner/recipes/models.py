from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    spoonacular_hash = models.CharField(max_length=255, blank=True, null=True)
    spoonacular_password = models.CharField(max_length=255, blank=True, null=True)
    spoonacular_username = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username
