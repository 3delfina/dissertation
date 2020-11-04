# forms.py
from django import forms
from .models import *


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['participant_id', 'participant_photo']
        
