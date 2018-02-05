from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . import models
from . import forms
@login_required
def index(request):
    #return HttpResponse('profile')
    EventsList = request.user.event_set.all()
    return render(request, 'rsvp/profile.html', {'EventsList':EventsList})
@login_required
def create_event(request):
    if request.method == 'POST':
        form = forms.CreateEventForm(request.POST)
        if form.is_valid():
            NewEvent = form.save()
            return redirect('event', id=NewEvent.pk)
    else:
            form = forms.CreateEventForm()
    return render(request, 'rsvp/create_event.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            #return HttpResponse('what')
            return redirect('index')
    else:
        form = UserCreationForm()

    #return HttpResponse("signup")
    return render(request, 'registration/signup.html', {'form': form})
