import os

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
# models.py


def is_positive(value):
    if not value.isdigit():
        raise ValidationError(
            _('%(value)s is not a non-negative integer.'),
            params={'value': value},
        )


def get_image_path(instance, filename):
    # images will be uploaded to <MEDIA_ROOT>/<participant_id>/<filename>
    return os.path.join(instance.participant.participant_id, filename)


class Participant(models.Model):
    participant_id = models.CharField(max_length=50, unique=True, validators=[is_positive])
    last_photo_id = models.IntegerField(default=0)

    def __str__(self):
        return self.participant_id


class Photo(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    participant_photo = models.ImageField(upload_to=get_image_path, max_length=250)
    faces_location_arr = models.CharField(max_length=400, blank=True)
    face_count = models.IntegerField(default=0, blank=True)
    participant_faces = models.ImageField(blank=True, max_length=250)
    participant_blur = models.ImageField(blank=True, max_length=250)
    participant_pixel = models.ImageField(blank=True, max_length=250)
    participant_deepfake = models.ImageField(blank=True, max_length=250)
    deepfake_all = models.ImageField(blank=True, max_length=250)
