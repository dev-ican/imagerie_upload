from django import forms
# from django.core.validators import *
# from django.http import *
# from datetime import date
# from bootstrap_datepicker_plus import DatePickerInput
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class LogIn(forms.Form):
    ''' Formulaire pour se loguer '''
    log_id = forms.CharField(label='Identifiant', max_length=100)
    pwd = forms.CharField(label='Mot de passe',
                          widget=forms.PasswordInput(),
                          max_length=100
                          )


class UploadForm(forms.Form):
    ''' Formulaire de chargement de fichier '''
    nip = forms.CharField(label='Numéro patient', max_length=100)
    etudes = forms.ChoiceField(widget=forms.Select(), choices=(['liste de vos études']), initial='0', required=True,)
    date_irm = forms.DateField(label="Date de l'examen", widget=DateTimePickerInput(format='%Y-%m-%d'), required=True)
    upload = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))



