from django.db import models


# Create your models here.
# models.py

class Participant(models.Model):
    participant_id = models.CharField(max_length=50, unique=True)
    participant_photo = models.ImageField(upload_to='images/')
    faces_location_arr = models.CharField(max_length=200, blank=True)
    face_count = models.IntegerField(default=0, blank=True)
    participant_faces = models.ImageField(upload_to='images/faces', blank=True)
    participant_blur = models.ImageField(upload_to='images/blur', blank=True)
    participant_pixel = models.ImageField(upload_to='images/pixel', blank=True)

    def __str__(self):
        return self.participant_id
