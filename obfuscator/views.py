from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView
from .obfuscate import blur_image, pixelate_image, deepfake_image, number_faces
from .forms import ParticipantForm, FacesForm
from .models import Participant
from django.conf import settings

import ast
import cv2
import os


def _get_file_paths(filename_original, filename_addition, dirname):
    original_path = os.path.join(settings.MEDIA_ROOT, filename_original)
    obfuscation_filename = filename_original.replace(".", filename_addition) \
        .replace("images", dirname)
    obfuscation_path = os.path.join(settings.MEDIA_ROOT, obfuscation_filename)
    return original_path, obfuscation_path, obfuscation_filename


def get_blur(participant, faces):
    original_path, obfuscation_path, obfuscation_filename = _get_file_paths(participant.participant_photo.name,
                                                                            "_participant_blur.", "images/blur")
    blur_image(original_path, obfuscation_path, faces)
    participant.participant_blur = obfuscation_filename
    return participant


def get_pixelation(participant, face_choices_int):
    original_path, obfuscation_path, obfuscation_filename = _get_file_paths(participant.participant_photo.name,
                                                                            "_participant_pixel.", "images/pixel")
    pixelate_image(original_path, obfuscation_path, face_choices_int)
    participant.participant_pixel = obfuscation_filename
    return participant


def get_deepfake(participant, face_choices_int):
    original_path, obfuscation_path, obfuscation_filename = _get_file_paths(participant.participant_photo.name,
                                                                            "_participant_deepfake.", "images/deepfake")
    deepfake_image(original_path, obfuscation_path, face_choices_int)
    participant.participant_deepfake = obfuscation_filename
    return participant


def locate_faces(participant):
    original_path, obfuscation_path, obfuscation_filename = _get_file_paths(participant.participant_photo.name,
                                                                            "_participant_faces.", "images/faces")
    faces_str, count = number_faces(original_path, obfuscation_path)
    participant.face_count = count
    participant.faces_location_arr = faces_str
    participant.participant_faces = obfuscation_filename
    return participant


def index(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST, request.FILES)

        # TODO: ask for user's permission to save photo
        if form.is_valid():
            participant = form.save()

            participant = locate_faces(participant)
            participant.save()
            # return render(request, 'obfuscator/display.html', {'participant': participant})
            return redirect('display', participant.participant_id)
    else:
        form = ParticipantForm()
    return render(request, "obfuscator/index.html", {'form': form})


def display(request, participant_id):
    participant = Participant.objects.get(participant_id=participant_id)
    form = FacesForm(participant.face_count, request.POST)
    context = {'participant': participant, 'form': form}

    if form.is_valid():
        face_choices = form.cleaned_data['face_choices']
        all_faces = ast.literal_eval(participant.faces_location_arr)
        chosen_faces = [all_faces[int(i) - 1] for i in face_choices]
        participant = get_blur(participant, chosen_faces)
        participant = get_pixelation(participant, chosen_faces)
        participant = get_deepfake(participant, chosen_faces)
        participant.save()
        context["display"] = 1
        return render(request, 'obfuscator/display.html', context)

    return render(request, 'obfuscator/display.html', context)
