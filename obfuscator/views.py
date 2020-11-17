from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView
from .obfuscate  import blur_image, pixelate_image
from .forms import ParticipantForm
from .models import Participant
from django.conf import settings
import os


def get_blur(participant):
    print("Inside get blur")
    photo_filename = participant.participant_photo.name
    blur_path = os.path.join(settings.MEDIA_ROOT, photo_filename.replace(".", "_participant_blur."))
    blur_path = blur_path.replace("images", "images/blur")

    #image = cv2.imread(participant.participant_photo)
    blur_image(os.path.join(settings.MEDIA_ROOT, photo_filename), blur_path)
    participant.participant_blur = photo_filename.replace(".", "_participant_blur.").replace("images", "images/blur")
    return participant

def get_pixelation(participant):
    print("Inside get pixelation")
    photo_filename = participant.participant_photo.name
    pixel_path = os.path.join(settings.MEDIA_ROOT, photo_filename.replace(".", "_participant_pixel."))
    pixel_path = pixel_path.replace("images", "images/pixel")

    #image = cv2.imread(participant.participant_photo)
    pixelate_image(os.path.join(settings.MEDIA_ROOT, photo_filename), pixel_path)
    participant.participant_pixel = photo_filename.replace(".", "_participant_pixel.").replace("images", "images/pixel")
    return participant


def index(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST, request.FILES)

        # TODO: ask for user's permission to save photo
        if form.is_valid():
            participant = form.save()
            participant = get_blur(participant)
            participant = get_pixelation(participant)
            participant.save()
            context = {'participant': participant}
            return render(request, 'obfuscator/display.html', context)
            # return redirect('display', participant_id)
    else:
        form = ParticipantForm()
    return render(request, "obfuscator/index.html", {'form': form})

def process():
    # TODO: prepare various obfuscation results
    pass
