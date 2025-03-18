from django import forms
from .models import GroundRegistration, Host_Tournament

class GroundRegistrationForm(forms.ModelForm):
    class Meta:
        model = GroundRegistration
        fields = ['ground_name', 'ground_location', 'ground_address', 'ground_desc', 'ground_feature', 'ground_rate', 'ground_img', 'ground_type', 'is_available']

class HostTournamentForm(forms.ModelForm):
    class Meta:
        model = Host_Tournament
        fields = ['tournament_name', 'tournament_date', 'tournament_desc', 'tournament_rate', 'is_available']