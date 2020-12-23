from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import time

# Create your models here.
# models.py

def is_positive(value):
    if not value.isdigit():
        raise ValidationError(
            _('%(value)s is not a non-negative integer.'),
            params={'value': value},
        )

class Participant(models.Model):
    participant_id = models.CharField(max_length=50, unique=True, validators=[is_positive])
    participant_photo = models.ImageField(upload_to='images/')
    faces_location_arr = models.CharField(max_length=200, blank=True)
    face_count = models.IntegerField(default=0, blank=True)
    participant_faces = models.ImageField(upload_to='images/faces', blank=True)
    participant_blur = models.ImageField(upload_to='images/blur', blank=True)
    participant_pixel = models.ImageField(upload_to='images/pixel', blank=True)
    participant_deepfake = models.ImageField(upload_to='images/deepfake', blank=True)

    def __str__(self):
        return self.participant_id
