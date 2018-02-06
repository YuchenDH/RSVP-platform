from django import forms
from . import models
from django.contrib.auth.models import User
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput

class CreateEventForm(forms.ModelForm):
    class Meta:
        model = models.Event
        fields = [
            'title',
            'date_and_time',
            'summary',
            'plus',
        ]

class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = [
            'description',
        ]

class CreateOptionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = [
            'description',
        ]

class TextForm(forms.Form):
    text = forms.CharField(label='text', max_length=100)
