from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *


# class AuthForm(forms.Form):
#     email = forms.CharField(max_length=30, widget=forms.Textarea(attrs={'cols': 30, 'rows': 5}))
#     password = forms.CharField(max_length=250)

class AuthForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={"class": "input-email", "placeholder": "email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input-password", "placeholder": "password"}))
