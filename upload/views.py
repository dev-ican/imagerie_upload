from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.files import File

from .forms import UploadForm
from .models import RefEtudes, JonctionUtilisateurEtude, SuiviUpload, RefControleQualite

from datetime import date, time, datetime

# Create your views here.

@login_required(login_url="/auth/auth_in/")
def index(request):

		return render(request,
				  'index.html')

@login_required(login_url="/auth/auth_in/")
def contact(request):

		return render(request,
				  'contact.html')

@login_required(login_url="/auth/auth_in/")
def formulaire(request):
	user_current = request.user
	liste_protocole = []

	if request.method == 'POST':
		form_instance = UploadForm(request.POST,request.FILES)
		etude = request.POST["etudes"]
		nip = request.POST["nip"]
		date = request.POST["date_irm"]
		info = request.FILES

		id_etude = JonctionUtilisateurEtude.objects.filter(id__exact=etude)
		id_qc = RefControleQualite.objects.get(id__exact=3)

		date_now = datetime.now()
		create_suivi = SuiviUpload(user=user_current, etude=id_etude[0], id_patient=nip, date_upload=date_now.date(), date_examen=date, controle_qualite=id_qc, fichiers=request.FILES['upload'])
		create_suivi.save()

	form = UploadForm()
	request_utilisateur_protocole = JonctionUtilisateurEtude.objects.filter(user__exact=user_current.id)

	for util_pro in request_utilisateur_protocole:
		collapse = (util_pro.id,util_pro.etude.nom)
		liste_protocole.append(collapse)

	liste_protocole.append((0,"Séléctionner une étude"))
	print(liste_protocole)
	form.fields['etudes'].choices = liste_protocole
	form.fields['etudes'].initial = [0]

	return render(request, 'form_upload.html', {'form': form})




