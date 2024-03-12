from django.db import models
from django.contrib.auth.models import AbstractUser

class CarSeekUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('renter', 'renter'),
        ('dealer', 'dealer'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    drivers_license = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self) -> str:
        return self.username

class UnavailableDate(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE, related_name='unavailable_dates')
    date = models.DateField()

class Car(models.Model):
    brand = models.CharField(max_length=50)
    posted_by = models.ForeignKey(CarSeekUser, on_delete=models.CASCADE)
    model = models.CharField(max_length=50)
    rental_rate_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    not_available_on = models.ManyToManyField(UnavailableDate, blank=True, related_name='cars_with_unavailable_dates')
    location = models.CharField(max_length=10)  # Adjust the max_length as needed

    image = models.ImageField(upload_to='car_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.posted_by} {self.brand} {self.model}"
    
class RentalAgreement(models.Model):
    renter = models.ForeignKey(CarSeekUser, on_delete=models.CASCADE, blank=False, null=False)
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING, related_name='rented_cars')

    rental_start_date = models.DateField()
    rental_end_date = models.DateField()

    def __str__(self):
        return f"Rental Agreement for {self.car.brand} {self.car.model} {self.car.posted_by.username} - Renter: {self.renter.username}"
    