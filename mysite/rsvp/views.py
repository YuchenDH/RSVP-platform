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
def event(request, id):
    #show event detail
    Object = request.user.event_set.filter(pk=id).all()
    if Object:
        QuestionList = Object.question_set.all()
        context = {
            'event':Object,
            'question':QuestionList,
        }
        return render(request, 'rsvp/event.html', context)

@login_required
def create_event(request):
    if request.method == 'POST':
        form = forms.CreateEventForm(request.POST)
        if form.is_valid():
            NewEvent = form.save()
            NewEvent.owner.add(request.user)
            return redirect('index')
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
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def create_question(request, event_pk):
    if request.method == 'POST':
        form = QuestionCreationForm(request.POST)
        if form.is_valid():
            NewQuestion = form.save()
            NewQuestion.event = Event_set.filter(pk=event_pk).all
            NewQuestion.final = False
            return redirect('event', id=event_pk)
    else:
        form = forms.QuestionCreationForm()
    return render(request, 'rsvp/create_question.html', id=event_pk)

@login_required
def create_option(request, question_pk):
    if request.method == 'POST':
        form = OptionCreationForm(request.POST)
        if form.is_valid():
            NewOption=form.save()
            NewOption.question = Question_set.filter(pk=question_pk).all
            return redirect('event', id=Question.objects.get(pk=question_pk).event.pk)
    else:
        form = forms.OptionCreationForm()
    return render(request, 'rsvp/create_option.html', id=form.question.event.pk)

@login_required
def guest_response(request, event_pk):
    return HttpResponse('guest_response')
#takes event_pk look for the event
#validate whether the guest is in the guest group
#if validated, return the response page, passing the event_pk and user_pk as context
#else, show the permission denied page
