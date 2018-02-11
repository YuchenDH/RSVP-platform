from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from . import models
from . import forms
from  django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

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
    #permission validate
    try:
        event=models.Event.objects.get(pk=id)
        if event:
            if request.method == 'POST':
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
        return redirect('/rsvp/event/'+id)

@login_required
def add_vendor(request, id, role):
    try:
        event=models.Event.objects.get(pk=id)
        if event:
            if request.method == 'POST':
                form = forms.TextForm(request.POST)
                if form.is_valid:
                    NewRole = models.User.objects.get(username=request.POST['text'])
                    if (NewRole):
                        if role == 'vendor':
                            NewVendor = models.Vendor()
                            NewVendor.people = NewRole
                            NewVendor.event_id = id
                            NewVendor.save()
                        if role == 'guest':
                            NewGuest = models.Guest()
                            NewGuest.people = NewRole
                            NewGuest.event_id = id
                            NewGuest.save()
                        to_email = [NewRole.email,]
                        subject = "reminder from RSVP"
                        message = "You're invited to " + event.title + " as a " + role + ", go check it out!"
                        email(to_email, subject, message)
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
        event=models.Event.objects.get(pk=id)
        if event:
            if request.method == 'POST':
                form = forms.TextForm(request.POST)
                if form.is_valid:
                    NewQuestion = models.Question()
                    NewQuestion.description = request.POST['text']
                    NewQuestion.final = 0
                    NewQuestion.event = event
                    #NewQuestion.vendor = request.user
                    NewQuestion.userspecify = ('userspecify' in request.POST)
                    try:
                        CandVendor=event.vendor_set.filter(people=models.User.objects.get(username=request.POST['vendor']))
                        if not CandVendor.exists():
                            raise ObjectDoesNotExist
                        CandVendor=CandVendor.first().people
                    except:
                        CandVendor=request.user
                    NewQuestion.vendor=CandVendor
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
                    if (request.POST['text'] ==""):
                        NewOption.description = "Enter your answer"
                    else:
                        NewOption.description = request.POST['text']
                    NewOption.count = 0
                    NewOption.question = question
                    NewOption.original = True
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
        if question.vendor.pk == request.user.pk:
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
            #return redirect('index')
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

@login_required
def guest_response(request, id):
    event = models.Event.objects.get(pk=id)
    
    if request.method == 'POST':
        guest = event.guest_set.get(people=request.user)
        if request.POST['response'] == 'zero':
            guest.response = -1
            guest.save()
            return redirect('index')
        elif request.POST['response'] == 'one' or request.POST['response'] == 'two':
            guest.response = 1
            guest.save()
            QuestionList = event.question_set.all()
            for question in QuestionList:
                if str(question.pk) in request.POST:
                    if request.POST[str(question.pk)]=="-1":
                        if question.userspecify:
                            option = models.Option()
                            option.description=request.POST[str(question.pk)+'user']
                            option.question=question
                            option.count=1
                            option.original=False
                            option.save()
                            option.people.add(request.user)
                            option.save()
                    else:
                        option = models.Option.objects.get(pk=int(request.POST[str(question.pk)]))
                        print(option.description)
                        print(request.user)
                        option.people.add(request.user)
                        option.count+=1
                        option.save()
                        #print(option.people.all())
            context = {
                'Plus':'1',
            }
            if request.POST['response'] == 'two':
                guest.response = 1
                guest.save()
                return render(request, 'rsvp/response_plus.html', {'event':event})
            return redirect('event', id=id)
        else:
            return HttpResponse('Bad Request', 500)
        return HttpResponse(request.POST, 400)
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
        is_owner(request.user, event)
        question = event.question_set.get(pk=qid)
        question.delete()
    except:
        return HttpResponse(403)
    return redirect('event', id=id)

@login_required
def remove_option(request, id, oid):
    try:
        event = models.Event.objects.get(pk=id)
        is_owner(request.user, event)
        option = models.Option.objects.get(pk=oid)
        option.delete()
    except ObjectDoesNotExist as e:
        return HttpResponse(e,403)
    return redirect('event', id=id)
            

@login_required
def edit_question(request, id, qid):
    if request.method == 'POST':
        try:
            event = models.Event.objects.get(pk=id)
            question = event.question_set.get(pk=qid)
            is_owner(request.user, event)
            if forms.TextForm(request.POST).is_valid:
                question.description=request.POST['text']
                question.save()
                to_email = []
                subject = "reminder from RSVP"
                message = "The quesetionaire of " + event.title + " is changed. Go and check it out"
                for guest in event.guest_set.all():
                    to_email.append(guest.people.email)
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
            is_owner(request.user, event)
            if forms.TextForm(request.POST).is_valid:
                option.description=request.POST['text']
                option.save()
                to_email = []
                subject = "reminder from RSVP"
                message = "The quesetionaire of " + event.title + " is changed. Go and check it out"
                for guest in event.guest_set.all():
                    to_email.append(guest.people.email)
                email(to_email, subject, message)
        except ObjectDoesNotExist:
            return HttpResponse(404)
        return redirect('event', id=id)

@login_required
def view_response(request, id):
    event = models.Event.objects.get(pk=id)
    OptionList = []
    if event.owner.filter(pk=request.user.pk).exists():
        QuestionList=event.question_set.all()
        Guest=False
    elif event.vendor_set.filter(people=request.user).exists():
        QuestionList=event.question_set.filter(vendor=request.user)
        Guest=False
        print(QuestionList)
    elif event.guest_set.filter(people=request.user).exists():
        QuestionList=event.question_set.all()
        for q in QuestionList:
            for i in q.option_set.filter(people=request.user):
                OptionList+=[i]
        Guest=True
    else:
        return HttpResponse(403)
    context={
        'question_list':QuestionList,
        'is_guest':Guest,
        'option_list':OptionList,
    }
    return render(request, 'rsvp/view_response.html', context)

@login_required
def edit_response(request, id):
    event = models.Event.objects.get(pk=id)
    is_guest(request.user, event)
    try:
        for question in event.question_set.all():
            for option in question.option_set.all():
                if option.people.filter(pk=request.user.pk).exists() and option.original:
                    option.people.remove(request.user)
                    option.save()
                else:
                    option.delete()
        form = forms.ResponseForm()
        context = {'event':event,
                   'form':form,
            }
        return render(request, 'rsvp/response.html', context)
    except:
        return HttpResponse(403)
