from django import forms
from django.core.validators import *
from django.http import *
from datetime import date

from upload.models import *


class ContactForm(forms.Form):
	nom = forms.CharField(label='Nom du collaborateur', max_length=3000)
	prenom = forms.CharField(label='Prénom du collaborateur', max_length=3000)
	email = forms.EmailField(
		label="Courriel du collaborateur",
		max_length=1000,
		validators=[
			EmailValidator()])
	telephone = forms.IntegerField(label="Numéro de téléphone")
	poste = forms.CharField(label='Nom du poste', max_length=3000)



