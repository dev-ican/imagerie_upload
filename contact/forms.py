# -*- coding: utf-8 -*-

from datetime import date

from django import forms
from django.core.validators import *
from django.http import *

from upload.models import *


class ContactForm(forms.Form):
    """Formulaire de contact."""

    nom = forms.CharField(
        label="Nom du collaborateur", max_length=3000
    )
    prenom = forms.CharField(
        label="Prénom du collaborateur", max_length=3000
    )
    email = forms.EmailField(
        label="Courriel du collaborateur",
        max_length=1000,
        validators=[EmailValidator()],
    )
    telephone = forms.CharField(
        label="Numéro de téléphone",
        max_length=12,
        validators=[
            RegexValidator(
                regex="([0-9])+",
                message="Numero de téléphone valide",
            )
        ],
    )
    poste = forms.CharField(
        label="Nom du poste", max_length=3000
    )
