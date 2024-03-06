# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CarSeekUser

class CarSeekUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CarSeekUser
        fields = UserCreationForm.Meta.fields + ('user_type', 'drivers_license',)
