from django.forms import ModelForm
from . import models
from django.contrib.auth.models import User
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput

class CreateEventForm(ModelForm):
    class Meta:
        model = models.Event
        fields = [
            'title',
            'date_and_time',
            'summary',
            'plus',
        ]

class CreateQuestionForm(ModelForm):
    class Meta:
        model = models.Question
        fields = [
            'description',
        ]

class CreateOptionForm(ModelForm):
    class Meta:
        model = models.Question
        fields = [
            'description',
        ]