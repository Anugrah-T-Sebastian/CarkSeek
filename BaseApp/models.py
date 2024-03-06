from django.db import models
from django.contrib.auth.models import AbstractUser

class CarSeekUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('renter', 'renter'),
        ('dealer', 'dealer'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    drivers_license = models.CharField(max_length=16, blank=False, null=False)

    def __str__(self) -> str:
        return self.username
    