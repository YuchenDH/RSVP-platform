from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.template.context import RequestContext

from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from bootstrap_toolkit.widgets import BootstrapUneditableInput
from django.contrib.auth.decorators import login_required

from .forms import LoginForm
# Create your views here.

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'auth/login.html')

def register(request):
    return HttpResponse("This is the register page")
