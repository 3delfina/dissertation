from django.shortcuts import render, redirect
from .obfuscate import blur_image, pixelate_image, deepfake_image, deepfake_and_number, mask_image, avatar_image
from .forms import ParticipantForm, FacesForm, PhotoForm, PhotoReuploadForm
from .models import Participant, Photo
from django.conf import settings
from django.shortcuts import get_object_or_404

import ast
import os
import logging

logger = logging.getLogger()


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
    pixelate_image(original_path, obfuscation_path, face_choices_int)
    photo.participant_pixel = obfuscation_filename
    return photo


def get_deepfake(photo, not_chosen):
    original_path, obfuscation_path, obfuscation_filename = _get_file_paths(photo.participant_photo.name,
                                                                            "_participant_deepfake.")
    img_deepfake_all = photo.deepfake_all
    deepfake_image(original_path, obfuscation_path, img_deepfake_all, not_chosen)
    photo.participant_deepfake = obfuscation_filename
    return photo


def get_masked(photo, face_choices_int):
    original_path, obfuscation_path, obfuscation_filename = _get_file_paths(photo.participant_photo.name,
                                                                            "_participant_masked.")
    mask_image(original_path, obfuscation_path, face_choices_int)
    photo.participant_masked = obfuscation_filename
    return photo


def get_avatar(photo, face_choices_int):
    original_path, obfuscation_path, obfuscation_filename = _get_file_paths(photo.participant_photo.name,
                                                                            "_participant_avatar.")
    avatar_image(original_path, obfuscation_path, face_choices_int)
    photo.participant_avatar = obfuscation_filename
    return photo


def get_deepfake_all(photo):

    original_path, obfuscation_path, deepfake_filename = _get_file_paths(photo.participant_photo.name,
                                                                            "_participant_deepfake_all.")
    _, faces_path, faces_filename = _get_file_paths(photo.participant_photo.name,
                                                                            "_participant_faces.")
    faces_str, count = deepfake_and_number(original_path, obfuscation_path, faces_path)
    photo.deepfake_all = deepfake_filename
    photo.face_count = count
    photo.faces_location_arr = faces_str
    photo.participant_faces = faces_filename
    return photo


# def locate_faces(photo):
#     original_path, obfuscation_path, obfuscation_filename = _get_file_paths(photo.participant_photo.name,
#                                                                             "_participant_faces.")
#     faces_str, count = number_faces(original_path, obfuscation_path)
#     photo.face_count = count
#     photo.faces_location_arr = faces_str
#     photo.participant_faces = obfuscation_filename
#     return photo


def index(request):
    if request.method == 'POST':
        participant_form = ParticipantForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)

        if participant_form.is_valid() and photo_form.is_valid():
            participant = participant_form.save()
            participant.save()
            photo = photo_form.save(commit=False)
            photo.participant = participant
            photo.save()
            photo = get_deepfake_all(photo)
            photo.save()
            participant.last_photo_id = photo.id
            participant.save()
            # return render(request, 'obfuscator/display.html', {'participant': participant})
            create_session(request, participant.id)
            return redirect('display')
    else:
        participant_form = ParticipantForm()
        photo_form = PhotoForm()
    return render(request, "obfuscator/index.html", {
        'participant_form': participant_form,
        'photo_form': photo_form})


def display(request):
    id = access_session(request)
    logger.info("participant_id is:" + str(id))
    participant = get_object_or_404(Participant, pk=id)
    # participant = Participant.objects.get(participant_id=participant_id)
    photo = Photo.objects.get(id=participant.last_photo_id)

    form = FacesForm(photo.face_count, request.POST)
    photo_form = PhotoReuploadForm(request.POST, request.FILES)
    context = {'participant': participant, 'photo': photo, 'form': form, 'photo_form': photo_form}

    if form.is_valid():
        face_choices = form.cleaned_data['face_choices']
        all_faces = ast.literal_eval(photo.faces_location_arr)
        chosen_faces = [all_faces[int(i) - 1] for i in face_choices]

        not_chosen = []
        for i in range(1, len(all_faces) + 1):
            if str(i) not in set(face_choices):
                not_chosen.append(all_faces[i - 1])
        photo = get_blur(photo, chosen_faces)
        photo = get_pixelation(photo, chosen_faces)
        photo = get_deepfake(photo, not_chosen)
        photo = get_masked(photo, chosen_faces)
        photo = get_avatar(photo, chosen_faces)
        photo.save()
        context["display"] = 1
        return render(request, 'obfuscator/display.html', context)

    elif photo_form.is_valid():
        photo = photo_form.save(commit=False)
        photo.participant = participant
        photo.save()
        photo = get_deepfake_all(photo)
        photo.save()
        participant.last_photo_id = photo.id
        participant.save()
        return redirect('display')

    context["display"] = 1 if photo.participant_deepfake else 0
    return render(request, 'obfuscator/display.html', context)


def create_session(request, session_id):
    delete_session(request)
    request.session['id'] = session_id


def access_session(request):
    return request.session.get('id')


def delete_session(request):
    try:
        del request.session['id']
    except KeyError:
        pass
