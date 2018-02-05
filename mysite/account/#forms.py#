from django import forms
from django.contrib.auth.models import User
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput

class LoginForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = u"Username",
        error_messages = {'required': 'Please input your username'},
        widget = forms.TextInput(
            attrs={
                'placeholder':u"Username",
            }
        ),
    )

    password = forms.CharField(
        required = True,
        label = u"Password",
        error_messages = {'required': u'Please input your password'},
        widget = forms.PasswordInput(
            attrs={
                'placeholder':u"Password",
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"Please input your username and password.")
        else:
            cleaned_data = super(LoginForm, self).clean()

            
class RegisterForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = u"Username",
        error_messages = {'required': 'Please input your username'},
        widget = forms.TextInput(
            attrs={
                'placeholder':u"Username",
            }
        ),
    )

    password = forms.CharField(
        required = True,
        label = u"Password",
        error_messages = {'required': u'Please input your password'},
        widget = forms.PasswordInput(
            attrs={
                'placeholder':u"Password",
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"Please input your usernameand password.")
        else:
            cleaned_data = super(LoginForm, self).clean()
