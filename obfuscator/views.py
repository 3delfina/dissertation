from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView
from .forms import ParticipantForm
from .models import Participant


def index(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST, request.FILES)

        # TODO: ask for user's permission to save photo
        if form.is_valid():
            participant = form.save()
            context = {'participant': participant}
            return render(request, 'obfuscator/display.html', context)
            # return redirect('display', participant_id)
    else:
        form = ParticipantForm()
    return render(request, "obfuscator/index.html", {'form': form})

def process():
    # TODO: prepare various obfuscation results
    pass
