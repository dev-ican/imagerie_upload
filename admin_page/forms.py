from django import forms
from django.core.validators import *
from django.http import *
from datetime import date

from upload.models import *
    
class FormsEtude(forms.Form):
    nom = forms.CharField(label="Nom de l'étude", max_length=100)
    date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'yyyy-mm-dd'})) 

class FormsEtape(forms.Form):
    nom = forms.CharField(label="Nom de l'étape", max_length=100)
    etudes = forms.ChoiceField(widget=forms.Select(), choices=(['liste de vos études']), required=True)

class FormsAutorisation(forms.Form):
	user = forms.ChoiceField(widget=forms.Select(), choices=(
        ['liste des utilisateurs']), initial='0', required=True,)
	etude = forms.ChoiceField(widget=forms.Select(), choices=(
        ['liste des études']), initial='0', required=True,)
	date = forms.DateField() 

class FormsUser(forms.Form):
	username = forms.CharField(label="Identifiant", max_length=100)
	pass_first = forms.CharField(
        label='Votre mot de passe',
        widget=forms.PasswordInput,
        max_length=100,
        validators=[
            RegexValidator(
                regex="([a-zA-Z]){4,12}([0-9]){2,12}",
                message="Mot de passe invalide")])
	pass_second = forms.CharField(label='Répéter votre mot de passe',widget=forms.PasswordInput,max_length=100,validators=[RegexValidator(regex="([a-zA-Z]){4,12}([0-9]){2,12}",message="Mot de passe invalide")])
	email = forms.EmailField(
        label='Votre courriel',
        max_length=200,
        validators=[
            EmailValidator()])
	nom = forms.CharField(label="Nom du Centre", max_length=100)
	numero = forms.IntegerField()
	date = forms.DateField()
