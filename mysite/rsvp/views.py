from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect

def index(request):
    return render(request, 'rsvp/index.html')

