# forms.py
from django import forms
from .models import Participant, Photo
import time

class ParticipantForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Participant
        fields = ['participant_id']
        # widgets = {
        #     'participant_id': forms.TextInput(attrs={'disabled': True}),
        # }

    def __init__(self, *args, **kwargs):
        kwargs.update(initial={
            # time in milliseconds
            'participant_id':  int(round(time.time() * 1000))
        })

        super(ParticipantForm, self).__init__(*args, **kwargs)

class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['participant_photo']


class PhotoReuploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['participant_photo']
        # help_texts = {
        #     'participant_photo': '',
        # }

    def __init__(self, *args, **kwargs):
        super(PhotoReuploadForm, self).__init__(*args, **kwargs)
        self.fields['participant_photo'].label = "Changed your mind? Upload a different photo"

class FacesForm(forms.Form):
    required_css_class = 'required'

    def __init__(self, faces_count, *args, **kwargs):
        super(FacesForm, self).__init__(*args, **kwargs)
        face_choices = tuple((x, x) for x in range(1, faces_count + 1))
        self.fields['face_choices'] = forms.MultipleChoiceField(choices=face_choices,
                                                                widget=forms.CheckboxSelectMultiple())
        self.fields['face_choices'].label = "Select faces to obfuscate"
