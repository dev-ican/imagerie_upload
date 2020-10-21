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

# Gère la page statistique
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------

@login_required(login_url="/auth/auth_in/")
def adminpage(request):
	''' Permet d'afficher la page de statistique '''
	label_etude_final = []
	dict_etat = {}
	list_etude = RefEtudes.objects.all()
	list_etat = RefEtatEtape.objects.all()
	for etude in list_etude:
		exist_etude = SuiviUpload.objects.filter(etude__etude=etude.id).distinct('dossier')
		resume_etat = {}
		resume_etat['data'] = json.dumps({'nbr':[exist_etude.count()],'nom':[etude.nom]})
		if exist_etude.exists():
			for etat in list_etat:
				nbr_qc_ok = 0
				nbr_qc_not = 0
				nbr_qc_nw = 0
				for dossier in exist_etude:
					try:
						qc_dossier = DossierUpload.objects.get(id=dossier.dossier.id)
						if qc_dossier.controle_qualite.id == 1:
							nbr_qc_nw += 1
						elif qc_dossier.controle_qualite.id == 2:
							nbr_qc_ok += 1
						elif qc_dossier.controle_qualite.id == 3:
							nbr_qc_not += 1
					except ObjectDoesNotExist:
						#Enregistrement du log------------------------------------------------------------------------
						#---------------------------------------------------------------------------------------------
						nom_documentaire = " a provoqué une erreur le dossier patient n'existe pas"
						informationLog(request, nom_documentaire)
						#----------------------------------------------------------------------------------------------
						#----------------------------------------------------------------------------------------------
					nbr_etat = JonctionEtapeSuivi.objects.filter(upload__exact=dossier.dossier).filter(etat__exact=etat).count()
					resume_etat[etat.nom] = nbr_etat
			resume_etat['Nouveau'] = nbr_qc_nw
			resume_etat['Refused'] = nbr_qc_not
			resume_etat['Passed'] = nbr_qc_ok
			dict_etat[etude.nom] = resume_etat
	#Enregistrement du log------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------------
	nom_documentaire = " Affiche la page graphique"
	informationLog(request, nom_documentaire)
	#----------------------------------------------------------------------------------------------
	#----------------------------------------------------------------------------------------------
	return render(request,
		'admin_page.html', {"nbr_etat":dict_etat})


