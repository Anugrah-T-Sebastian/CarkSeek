# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CarSeekUser, Car, RentalAgreement

class CarSeekUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=(('dealer', 'Dealer'), ('renter', 'Renter')), label='Role')

    class Meta(UserCreationForm.Meta):
        model = CarSeekUser
        fields = UserCreationForm.Meta.fields + ('user_type',)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            self.add_error('password2', "Passwords do not match.")

        user_type = cleaned_data.get('user_type')
        if user_type not in dict(self.fields['user_type'].choices):
            self.add_error('user_type', "Invalid user type.")

        return cleaned_data

class CarDetailsUploadForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'rental_rate_per_day', 'location', 'image']

class RentalAgreementForm(forms.ModelForm):
    class Meta:
        model = RentalAgreement
        fields = ['rental_start_date', 'rental_end_date']