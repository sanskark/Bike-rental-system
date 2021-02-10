from django.db import models
from django.contrib.auth.models import AbstractUser

# from PIL import Image

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_dealer = models.BooleanField(default=False)

class Location(models.Model):
    location_id = models.IntegerField(primary_key=True, auto_created=True)
    location_name = models.CharField(max_length=30, default='')

    def __str__(self):
        return f'{self.location_name}'