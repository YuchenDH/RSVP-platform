from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from . import models
from . import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models.query import EmptyQuerySet

def is_owner(user, event):
    if not event.owner.filter(pk=user.pk).exists():
        raise ObjectDoesNotExist
    return True

def is_vendor(user, event):
    if not event.vendor_set.filter(people=user).exists():
        raise ObjectDoesNotExist
    return True

def is_guest(user, event):
    if not event.guest_set.filter(people=user).exists():
        raise ObjectDoesNotExist
    return True

def email(to_email, subject, message):
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, to_email, fail_silently=False)
    
@login_required
def index(request):
    #return HttpResponse('profile')
    EventsList = request.user.event_set.all()
    VendorList = request.user.vendor_set.all()
    GuestList = request.user.guest_set.all()
    context = {
        'EventsList':EventsList,
        'VendorList':VendorList,
        'GuestList':GuestList,
        }
    return render(request, 'rsvp/profile.html', context)

@login_required
def event(request, id):
    #show event detail
    Object = models.Event.objects.get(pk=id)
    if Object:
        QuestionList = Object.question_set.all()
        try:
            is_owner(request.user, Object)
            editable=True
        except:
            editable=False
        context = {
            'event':Object,
            'question':QuestionList,
            'editable':editable,
        }
        if request.method=='GET':
            return render(request, 'rsvp/event.html', context)
        elif request.method=='POST':
            return render(request, 'rsvp/edit_event.html', context)
    else:
        return HttpResponse(404)

@login_required
def event_update(request, id):
    if request.method=='POST':
        Object = request.user.event_set.get(pk=id)
        try:
            is_owner(request.user, Object)
        except:
            return HttpResponse(403)
        if Object :
            form = forms.CreateEventForm(request.POST)
            if form.is_valid:
                Object.title = request.POST['title']
                Object.summary = request.POST['summary']
                Object.date_and_time = request.POST['date_and_time']
                Object.save()
            QuestionList = Object.question_set.all()
            context = {
                'event':Object,
                'question':QuestionList,
            }
            return render(request, '/rsvp/edit_event.html', context)
    return HttpResponse('404')
    
@login_required
def add_owner(request, id):
    try:
        event=models.Event.objects.get(pk=id)
        if event:
            if request.method == 'POST':
                is_owner(request.owner, event)
                form = forms.TextForm(request.POST)
                if form.is_valid:
                    NewRole = models.User.objects.get(username=request.POST['text'])
                    if (NewRole):
                        event.owner.add(NewRole)
                        return redirect('/rsvp/event/'+id, method='POST')
                return HttpResponse(404)
            else:
                return render(request, 'rsvp/add_user.html', form=forms.UsernameForm)
        else:
            return HttpResponse(404)
    except ObjectDoesNotExist as e:
        return HttpResponse(e, 404)

@login_required
def add_vendor(request, id, role):
    try:
        event=models.Event.objects.get(pk=id)
        if event:
            is_owner(request.user, event)
            if request.method == 'POST':
                form = forms.TextForm(request.POST)
                if form.is_valid:
                    NewRole = models.User.objects.get(username=request.POST['text'])
                    if (NewRole):
                        if role == 'vendor':
                            if is_vendor(NewRole, event):
                                pass
                            else:
                                NewVendor = models.Vendor()
                                NewVendor.people = NewRole
                                NewVendor.event_id = id
                                NewVendor.save()
                        if role == 'guest':
                            if is_guest(NewRole, event):
                                pass
                            else:
                                NewGuest = models.Guest()
                                NewGuest.people = NewRole
                                NewGuest.event_id = id
                                NewGuest.response = 0
                                NewGuest.save()
                        return redirect('/rsvp/event/'+id)
                return HttpResponse(404)
            else:
                return render(request, 'rsvp/add_user.html', form=forms.UsernameForm)
        else:
            return HttpResponse(404)
    except ObjectDoesNotExist as e:
        return redirect('/rsvp/event/'+id)

@login_required
def add_question(request, id):
    try:
        event = models.Event.objects.get(pk=id)
        if event:
            if request.method == 'POST':
                form = forms.TextForm(request.POST)
                if form.is_valid:
                    NewQuestion = models.Question()
                    NewQuestion.description = request.POST['text']
                    NewQuestion.final = 0
                    NewQuestion.event = event
                    try:
                        CandVendor=event.vendor_set.filter(people=models.User.objects.get(username=request.POST['vendor'])).first()
                        if not CandVendor:
                            raise ObjectDoesNotExist
                    except:
                        CandVendor=event.vendor_set.get(people=request.user)
                    NewQuestion.Vendor_id=CandVendor.pk
                    NewQuestion.userspecify = 'userspecify' in request.POST
                    NewQuestion.save()
                    QuestionList = event.question_set.all()
                    context = {
                        'event':event,
                        'question':QuestionList,
                    }
                    return render(request, 'rsvp/edit_event.html', context)
                return HttpResponse(404)
        else:
            return HttpResponse(404)
    except ObjectDoesNotExist as e:
        return HttpResponse(e, 404)
        return redirect('/rsvp/event/'+id)

@login_required
def add_option(request, id, qid):
    try:
        event=models.Event.objects.get(pk=id)
        question = event.question_set.get(pk=qid)
        if event and question :
            if request.method == 'POST':
                form = forms.TextForm(request.POST)
                if form.is_valid:
                    NewOption = models.Option()
                    NewOption.description = request.POST['text']
                    NewOption.count = 0
                    NewOption.question = question
                    NewOption.save()
                    QuestionList = event.question_set.all()
                    context = {
                        'event':event,
                        'question':QuestionList,
                    }
                    return render(request, 'rsvp/edit_event.html', context)
                return HttpResponse(404)
        else:
            return HttpResponse(404)
    except ObjectDoesNotExist as e:
        return redirect('/rsvp/event/'+id)

@login_required
def question_finalize(request, id, qid):
    try:
        event = request.user.event_set.get(pk=id)
        question = event.question_set.get(pk=qid)
        if event and question :
            if question.final == 0:
                question.final = 1
            else:
                question.final = 0
            question.save()
            return redirect('/rsvp/event/'+id)
        return HttpResponse(404)
    except ObjectDoesNotExist as e:
        return redirect('/rsvp/event/'+id)
    
@login_required
def create_event(request):
    if request.method == 'POST':
        form = forms.CreateEventForm(request.POST)
        if form.is_valid():
            NewEvent = form.save()
            NewEvent.owner.add(request.user)
            NewVendor = models.Vendor()
            NewVendor.people = request.user
            NewVendor.event = NewEvent
            NewVendor.save()
            return redirect('event', id=NewEvent.pk)
    else:
        form = forms.CreateEventForm()
    return render(request, 'rsvp/create_event.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = forms.UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
"""
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
def guest_response(request, id):
    if request.method == 'POST':
        form = forms.ResponseForm(request.POST)
        if form.is_valid():
            event = models.Event.objects.get(pk=id)
            guest = event.guest_set.get(people=request.user)
            if request.POST['response'] == '0':
                guest.response = -1
                guest.save()
                return redirect('index')
            else:
                guest.response = 1
                guest.save()
                QuestionList = event.question_set.all()
                context = {
                    'Plus':'1',
                    }
                return redirect('event', id=id)
        else:
            return HttpResponse(400)
#takes event_pk look for the event
#validate whether the guest is in the guest group
#if validated, return the response page, passing the event_pk and user_pk as context
#else, show the permission denied page
"""
@login_required
def guest_question(request, id):
    return
"""
    if request.method == 'POST':
        try:
            event = models.Event.objects.get(pk=id)
            if event:
                guest = event.guest_set.get(people=request.user)
                if guest.response == 1:
                    return render(request, 'rsvp/question.html')
                else:
                    raise ObjectDoesNotExist()
"""
@login_required
def guest_response(request, id):
    event = models.Event.objects.get(pk=id)
    if request.method == 'POST':
        guest = event.guest_set.get(people=request.user)
        if request.POST['response'] == '0':
            guest.response = -1
            guest.save()
            return redirect('index')
        else:
            guest.response = 1
            guest.save()
            
            
        return redirect('event', id=id)
    else:
        form = forms.ResponseForm()
        context = {'event':event,
                   'form':form,
               }
    return render(request, 'rsvp/response.html', context)

@login_required
def remove_question(request, id, qid):
    try:
        event = models.Event.objects.get(pk=id)
        is_owner(request, event)
        question = event.question_set.get(pk=qid)
        question.delete()
    except:
        return HttpResponse(403)
    return redirect('event', id=id)

@login_required
def remove_option(request, id, oid):
    try:
        event = models.Event.objects.get(pk=id)
        is_owner(request, event)
        option = models.Option.objects.get(pk=oid)
        option.delete()
    except:
        return HttpResponse(403)
    return redirect('event', id=id)
            

@login_required
def edit_question(request, id, qid):
    if request.method == 'POST':
        try:
            event = models.Event.objects.get(pk=id)
            question = event.question_set.get(pk=qid)
            is_owner(request, event)
            if forms.TextForm(request.POST).is_valid:
                question.description=request.POST['text']
                question.save()
                to_email = []
                subject = "reminder from RSVP"
                message = "The quesetionaire of " + event.title + " is changed. Go and check it out"
                for guest in event.guest_set.all():
                    to_email.append(guest.email)
                email(to_email, subject, message)
                #email
        except ObjectDoesNotExist:
            return HttpResponse(404)
        return redirect('event', id=id)

@login_required
def edit_option(request, id, oid):
    if request.method == 'POST':
        try:
            option = models.Option.objects.get(pk=oid)
            event = option.question.event
            is_owner(request, event)
            if forms.TextForm(request.POST).is_valid:
                option.description=request.POST['text']
                option.save()
                to_email = []
                subject = "reminder from RSVP"
                message = "The quesetionaire of " + event.title + " is changed. Go and check it out"
                for guest in event.guest_set.all():
                    to_email.append(guest.email)
                email(to_email, subject, message)
        except ObjectDoesNotExist:
            return HttpResponse(404)
        return redirect('event', id=id)
