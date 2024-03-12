from django.contrib import admin

from .models import CarSeekUser, Car, UnavailableDate, RentalAgreement

# Registered models 
admin.site.register(CarSeekUser)
admin.site.register(Car)
admin.site.register(UnavailableDate)
admin.site.register(RentalAgreement)
