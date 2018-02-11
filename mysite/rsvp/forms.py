from django import forms
from . import models
from django.contrib.auth.models import User
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput
from django.contrib.auth.forms import UserCreationForm

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            return user
        
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

class ResponseForm(forms.Form):
    response = forms.CharField(label='response', max_length=1)
