# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CarSeekUser, Car

class CarSeekUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CarSeekUser
        fields = UserCreationForm.Meta.fields + ('user_type', 'drivers_license',)

class CarDetailsUploadForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'rental_rate_per_day', 'location', 'image']