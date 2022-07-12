from django import forms
# from django.core.validators import *
# from django.http import *

# from upload.models import *

CHOICES=[(0,'Infos'),(1,'Protocoles')]

class DocumentForm(forms.Form):
	''' Formulaire d'enregistrement pour les documents '''
	titre = forms.CharField(label='Titre', max_length=500,)
	type = forms.ChoiceField(label="", choices=CHOICES, widget=forms.RadioSelect(attrs={'class': 'd-inline-flex'}))
	description = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 10}), label='Description', max_length=5000,)
	etudes = forms.ChoiceField(widget=forms.Select(), choices=(['liste de vos études']), initial='0', required=True,)
	document = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
