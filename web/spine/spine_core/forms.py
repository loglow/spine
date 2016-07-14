from django import forms
from django.contrib.auth.forms import AuthenticationForm 

class BootstrapAuthForm(AuthenticationForm):
    username = forms.CharField(
        max_length = 64,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control input-lg',
                'placeholder': 'Username',
            }
        )
    )
    password = forms.CharField(
        max_length = 64,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control input-lg',
                'type': 'password',
                'placeholder': 'Password',
            }
        )
    )