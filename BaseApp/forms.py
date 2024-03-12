# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CarSeekUser, Car, RentalAgreement

class CarSeekUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CarSeekUser
        fields = UserCreationForm.Meta.fields + ('user_type', 'drivers_license',)

class CarDetailsUploadForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'rental_rate_per_day', 'location', 'image']

class RentalAgreementForm(forms.ModelForm):
    class Meta:
        model = RentalAgreement
        fields = ['rental_start_date', 'rental_end_date']