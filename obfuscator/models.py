from django.db import models

# Create your models here.
# models.py

class Participant(models.Model):
    participant_id = models.CharField(max_length=50, unique=True)
    participant_photo = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.participant_id
