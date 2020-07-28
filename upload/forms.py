from django import forms
from django.core.validators import *
from django.http import *

from .models import *


class LogIn(forms.Form):
    log_id = forms.CharField(label='Identifiant', max_length=100)
    pwd = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(),
        max_length=100)

class FormUpload(forms.Form):
    info = forms.CharField(label='Info', max_length=100)
    infoB = forms.CharField(label='Info', max_length=100)
    infoT = forms.CharField(label='Info', max_length=100)
    protocoles = forms.ChoiceField(widget=forms.Select(), choices=(
        ['liste de vos protocoles']), initial='0', required=True,)
