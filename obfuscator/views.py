from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView
from .obfuscate import blur_image, pixelate_image, deepfake_image, number_faces
from .forms import ParticipantForm, FacesForm, PhotoForm, PhotoReuploadForm
from .models import Participant, Photo
from django.conf import settings

import ast
import cv2
import os


def _get_file_paths(filename_original, filename_addition):
    original_path = os.path.join(settings.MEDIA_ROOT, filename_original)
    obfuscation_filename = filename_original.replace(".", filename_addition)
    obfuscation_path = os.path.join(settings.MEDIA_ROOT, obfuscation_filename)
    return original_path, obfuscation_path, obfuscation_filename


def get_blur(photo, faces):
    original_path, obfuscation_path, obfuscation_filename = _get_file_paths(photo.participant_photo.name,
                                                                            "_participant_blur.")
    blur_image(original_path, obfuscation_path, faces)
    photo.participant_blur = obfuscation_filename
    return photo


def get_pixelation(photo, face_choices_int):
    original_path, obfuscation_path, obfuscation_filename = _get_file_paths(photo.participant_photo.name,
                                                                            "_participant_pixel.")
    print(original_path)
    print(obfuscation_path)
    pixelate_image(original_path, obfuscation_path, face_choices_int)
    photo.participant_pixel = obfuscation_filename
    return photo


def get_deepfake(photo, face_choices_int, not_chosen):
    original_path, obfuscation_path, obfuscation_filename = _get_file_paths(photo.participant_photo.name,
                                                                            "_participant_deepfake.")
    deepfake_image(original_path, obfuscation_path, face_choices_int, not_chosen)
    photo.participant_deepfake = obfuscation_filename
    return photo


def locate_faces(photo):
    original_path, obfuscation_path, obfuscation_filename = _get_file_paths(photo.participant_photo.name,
                                                                            "_participant_faces.")
    faces_str, count = number_faces(original_path, obfuscation_path)
    photo.face_count = count
    photo.faces_location_arr = faces_str
    photo.participant_faces = obfuscation_filename
    return photo


def index(request):
    if request.method == 'POST':
        participant_form = ParticipantForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)

        if participant_form.is_valid() and photo_form.is_valid():
            participant = participant_form.save()
            participant.save()
            photo = photo_form.save(commit = False)
            photo.participant = participant
            photo.save()
            photo = locate_faces(photo)
            photo.save()
            participant.last_photo_id = photo.id
            participant.save()
            # return render(request, 'obfuscator/display.html', {'participant': participant})
            return redirect('display', participant.participant_id)
    else:
        participant_form = ParticipantForm()
        photo_form = PhotoForm()
    return render(request, "obfuscator/index.html", {
                                        'participant_form': participant_form,
                                        'photo_form': photo_form})


def display(request, participant_id):
    participant = Participant.objects.get(participant_id=participant_id)
    photo = Photo.objects.get(id=participant.last_photo_id)

    form = FacesForm(photo.face_count, request.POST)
    photo_form = PhotoReuploadForm(request.POST, request.FILES)
    context = {'participant': participant, 'photo': photo, 'form': form, 'photo_form': photo_form}

    if form.is_valid():
        face_choices = form.cleaned_data['face_choices']
        all_faces = ast.literal_eval(photo.faces_location_arr)
        chosen_faces = [all_faces[int(i) - 1] for i in face_choices]
        print((all_faces))
        print((chosen_faces))
        not_chosen = []
        for i in range(1, len(all_faces)+1):
            if str(i) not in set(face_choices):
                not_chosen.append(all_faces[i-1])
        photo = get_blur(photo, chosen_faces)
        photo = get_pixelation(photo, chosen_faces)
        photo = get_deepfake(photo, chosen_faces, not_chosen)
        photo.save()
        context["display"] = 1
        return render(request, 'obfuscator/display.html', context)

    elif photo_form.is_valid():
        photo = photo_form.save(commit = False)
        photo.participant = participant
        photo.save()
        photo = locate_faces(photo)
        photo.save()
        participant.last_photo_id = photo.id
        participant.save()
        return redirect('display', participant.participant_id)

    return render(request, 'obfuscator/display.html', context)
