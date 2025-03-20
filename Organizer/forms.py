from django import forms
from .models import GroundRegistration, Host_Match,Reservation

class GroundRegistrationForm(forms.ModelForm):
    class Meta:
        model = GroundRegistration
        fields = ['ground_name', 'ground_location', 'ground_address', 'ground_desc', 'ground_feature', 'ground_rate', 'ground_img', 'ground_type', 'is_available']

class HostMatchForm(forms.ModelForm):
    class Meta:
        model = Host_Match
        fields = ['match_name', 'match_date', 'match_desc', 'match_rate', 'is_available']
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['full_name', 'contact_number', 'email', 'date', 'time_slot']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }