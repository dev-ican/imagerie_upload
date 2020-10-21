from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.files import File

from django.conf import settings
import os, tempfile
from admin_page.views.module_admin import *
from django.utils import timezone

from .forms import DocumentForm
from upload.models import RefEtudes, JonctionUtilisateurEtude, RefEtapeEtude, RefInfocentre, JonctionEtapeSuivi, RefEtatEtape, SuiviDocument, SuiviDocument, log, RefTypeAction

from datetime import date, time, datetime
# Create your views here.
@login_required(login_url="/auth/auth_in/")
def gestiondoc(request):

	if request.method == 'POST':
		date_now = timezone.now()
		titre = request.POST['titre']
		desc = request.POST['description']
		etude = request.POST['etudes']
		type = request.POST['type']
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		user_current = request.user
		type_action = RefTypeAction.objects.get(pk=7)
		nom_documentaire = 'Creation documentaire ' + str(titre)
		log.objects.create(user=user_current, action=type_action, date=date_now, info=nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
		if type == str(0):
			url_img = 'bg-nw-info.jpg'
		elif type == str(1):
			url_img = 'bg-nw-protocole.jpg'
		path_img = settings.BASE_DIR + url_img
		id_etude = RefEtudes.objects.get(id__exact=etude)
		date_now = timezone.now()
		user_current = request.user
		filez = request.FILES.getlist('document')
		for f in filez:
			create_suivi = SuiviDocument(user=user_current, etude=id_etude, titre=titre, description=desc, date=date_now, fichiers=f, background=url_img)
			create_suivi.save()
	form = DocumentForm()
	request_etude = RefEtudes.objects.all()
	liste_protocole = choiceEtude(True)
	form.fields['etudes'].choices = liste_protocole
	form.fields['etudes'].initial = [0]
	doc_tab = SuiviDocument.objects.all()
	return render(request,
		'admin_docu.html',{"form":form, 'resultat':doc_tab})

@login_required(login_url="/auth/auth_in/")
def downOnce(request, id):
	obj = SuiviDocument.objects.get(id__exact=id)
	filename = obj.fichiers.path
	#Enregistrement du log------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------------
	date_now = timezone.now()
	user_current = request.user
	type_action = RefTypeAction.objects.get(pk=4)
	nom_documentaire = 'Téléchargement du fichier : ' + str(filename)
	log.objects.create(user=user_current, action=type_action, date=date_now, info=nom_documentaire)
	#----------------------------------------------------------------------------------------------
	#----------------------------------------------------------------------------------------------
	file_path = os.path.join(settings.MEDIA_ROOT, filename)
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response

@login_required(login_url="/auth/auth_in/")
def docEdit(request, id):
	liste_protocole = []
	if request.method == 'POST':
		form = DocumentForm()
		titre = request.POST['titre']
		desc = request.POST['description']
		etude = request.POST['etudes']
		type = request.POST['type']
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		date_now = timezone.now()
		user_current = request.user
		type_action = RefTypeAction.objects.get(pk=2)
		nom_documentaire = 'Edition du document : ' + str(titre)
		log.objects.create(user=user_current, action=type_action, date=date_now, info=nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
		if type == str(0):
			url_img = 'bg-nw-info.jpg'
		elif type == str(1):
			url_img = 'bg-nw-protocole.jpg'
		SuiviDocument.objects.filter(id__exact=id).update(etude=etude, titre=titre, description=desc, background=url_img)
		filez = request.FILES.getlist('document')
		for f in filez:
			SuiviDocument.objects.filter(id__exact=id).update(fichiers=f)
		return HttpResponseRedirect('/admin_page/etudes/')
	else:
		obj = SuiviDocument.objects.get(id__exact=id)
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		date_now = timezone.now()
		user_current = request.user
		type_action = RefTypeAction.objects.get(pk=2)
		nom_documentaire = "Affichage de l'édition documentaire : " + str(obj.titre)
		log.objects.create(user=user_current, action=type_action, date=date_now, info=nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
		id_etude = RefEtudes.objects.get(nom=obj.etude)
		form = DocumentForm()
		request_etude = RefEtudes.objects.all()
		liste_protocole = choiceEtude(False)
		form.fields['etudes'].choices = liste_protocole
		form.fields['etudes'].initial = [id_etude.id]
		form.fields['titre'].initial = obj.titre
		form.fields['description'].initial = obj.description
		form.fields['document'].initial = obj.fichiers
	doc_tab = SuiviDocument.objects.all()
	return render(request,
		'admin_edit_docu.html',{"form":form, 'resultat':doc_tab, 'select':int(id)})

@login_required(login_url="/auth/auth_in/")
def docDeleted(request, id):
	obj = SuiviDocument.objects.get(id__exact=id)
	liste_protocole = []
	x = 0
	if request.method == 'POST':
		var_suivi = SuiviDocument.objects.get(id__exact=int(id))
		var_path = var_suivi.fichiers
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		date_now = timezone.now()
		user_current = request.user
		type_action = RefTypeAction.objects.get(pk=3)
		nom_documentaire = "Suppression du document : " + str(var_suivi.fichiers)
		log.objects.create(user=user_current, action=type_action, date=date_now, info=nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
		file_path = settings.MEDIA_ROOT + str(var_path)
		os.remove(file_path)
		var_suivi.delete()
		message = messages.add_message(
			request,
			messages.WARNING,
			"Suppression Faite")
	form = DocumentForm()
	liste_protocole = choiceEtude(True)
	form.fields['etudes'].choices = liste_protocole
	form.fields['etudes'].initial = [0]
	doc_tab = SuiviDocument.objects.all()
	context = {"form":form, 'resultat':doc_tab, 'message':message}
	return render(request,'admin_docu.html', context)
