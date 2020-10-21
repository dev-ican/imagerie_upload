from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.clickjacking import xframe_options_exempt

from django.conf import settings
from io import StringIO, BytesIO

from django.db.models import Count, Q
import json
import zipfile
import os, tempfile
from wsgiref.util import FileWrapper
from .module_views import *
from .module_log import *
from django.core.exceptions import ObjectDoesNotExist

from datetime import date, time, datetime
from django.utils import timezone
from .module_admin import checkmdp, take_data, choiceEtude, choiceCentre

from admin_page.forms import FormsEtude, FormsEtape, FormsAutorisation, FormsUser, FormsUserEdit, FormCentre
from upload.models import RefEtudes, JonctionUtilisateurEtude, RefEtapeEtude, RefInfocentre, JonctionEtapeSuivi, SuiviUpload, DossierUpload, RefEtatEtape, RefControleQualite, log, RefTypeAction

# Gère la partie Admin Etapes
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------

@login_required(login_url="/auth/auth_in/")
def adminetape(request):
	''' Charge la page index pour l'ajout ou l'édition d'une étape '''
	liste_protocole = []
	if request.method == 'POST':
		val_nom = request.POST['nom']
		val_etude = request.POST['etudes']
		query = RefEtudes.objects.get(id__exact=val_etude)
		RefEtapeEtude.objects.create(nom=val_nom, etude=query)
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		nom_documentaire = " a créé l'étape : " + nom
		creationLog(request, nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
	form = FormsEtape()
	request_etude = RefEtudes.objects.all()
	liste_protocole = choiceEtude(True)
	form.fields['etudes'].choices = liste_protocole
	form.fields['etudes'].initial = [0]
	etape_tab = RefEtapeEtude.objects.all()
	return render(request,
		'admin_etapes.html',{"form":form, 'resultat':etape_tab})

@login_required(login_url="/auth/auth_in/")
def etapeEdit(request, id_etape):
	''' Charge la page d'édition des étapes '''
	liste_protocole = []
	if request.method == 'POST':
		select_etape = RefEtapeEtude.objects.get(pk=id_etape)
		nom = request.POST['nom']
		etudes = request.POST['etudes']
		ref_etude = RefEtudes.objects.get(id=etudes)
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		nom_documentaire = " a editer l'étape etape/etude - etude édité/etape édité : " + select_etape.etude.nom + "/" + select_etape.nom + " - " + ref_etude.nom + "/" + nom
		editionLog(request, nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
		select_etape.nom = nom
		select_etape.etude = ref_etude
		select_etape.save()
		form = FormsEtape()
		return HttpResponseRedirect('/admin_page/etapes/')
	else:
		etape_filtre = RefEtapeEtude.objects.get(id=id_etape)
		id_etude = RefEtudes.objects.get(nom=etape_filtre.etude)
		form = FormsEtape()
		request_etude = RefEtudes.objects.all()
		liste_protocole = choiceEtude(False)
		form.fields['etudes'].choices = liste_protocole
		form.fields['etudes'].initial = [id_etude.id]
		form.fields['nom'].initial = etape_filtre.nom
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		nom_documentaire = " a ouvert l'édition pour l'étape etude/etape : " + etape_filtre.etude.nom + "/" + etape_filtre.nom
		informationLog(request, nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
	etape_tab = RefEtapeEtude.objects.all()
	return render(request,
		'admin_etapes_edit.html',{"form":form, 'resultat':etape_tab, 'select':int(id_etape)})

@login_required(login_url="/auth/auth_in/")
def etapeDel(request, id_etape):
	''' Appel Ajax permettant la supression d'une étapes '''
	liste_protocole = []
	x = 0
	if request.method == 'POST':
		suppr = True
		info_suivi = JonctionEtapeSuivi.objects.filter(etape__id__exact=id_etape)
		if info_suivi.exists():
			for nbr in info_suivi:
				x += 1
			suppr = False
		if suppr == True:
			id_log = RefEtapeEtude.objects.get(id__exact=id_etape)
			#Enregistrement du log------------------------------------------------------------------------
			#---------------------------------------------------------------------------------------------
			nom_documentaire = " a supprimé l'étude (etude/etape) : " + id_log.etude.nom + "/" + id_log.nom
			supprLog(request, nom_documentaire)
			#----------------------------------------------------------------------------------------------
			#---------------------------------------------------------------------------------------------
			RefEtapeEtude.objects.get(id__exact=id_etape).delete()
			message = messages.add_message(
				request,
				messages.WARNING,
				"Suppression Faite")
		else:
			id_log = RefEtapeEtude.objects.get(id__exact=id_etape)
			#Enregistrement du log------------------------------------------------------------------------
			#---------------------------------------------------------------------------------------------
			nom_documentaire = " à reçu un message d'erreur de suppression pour (etude/etape) : " + id_log.etude.nom + "/" + id_log.nom
			informationLog(request, nom_documentaire)
			#----------------------------------------------------------------------------------------------
			#---------------------------------------------------------------------------------------------
			message = messages.add_message(
				request,
				messages.WARNING,
				"Suppression annulée, cette étape est liée à :" + x + " suivi(s)")
	form = FormsEtape()
	liste_protocole = choiceEtude(True)
	form.fields['etudes'].choices = liste_protocole
	form.fields['etudes'].initial = [0]
	etape_tab = RefEtapeEtude.objects.all()
	context = {"form":form, 'resultat':etape_tab, 'message':message}
	return render(request,'admin_etapes.html', context)