from django import forms
from django.core.validators import *
from django.http import *

from .models import *


class LogIn(forms.Form):
    ''' Formulaire de connexion à l'application '''
    log_id = forms.CharField(label="Identifiant", max_length=100)
    pwd = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(),
        max_length=100,
    )
