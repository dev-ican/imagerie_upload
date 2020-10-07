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

from datetime import date, time, datetime
from .module_admin import checkmdp, take_data, choiceEtude, choiceCentre

from .forms import FormsEtude, FormsEtape, FormsAutorisation, FormsUser, FormsUserEdit, FormCentre
from upload.models import RefEtudes, JonctionUtilisateurEtude, RefEtapeEtude, RefInfocentre, JonctionEtapeSuivi, SuiviUpload, DossierUpload, RefEtatEtape, RefControleQualite


def gestionetape(dict_etape_nom,dict_etape_value,nbr_etape):
	if len(dict_etape_nom) == 0 or len(dict_etape_value) != nbr_etape:
		if len(dict_etape_value) != nbr_etape:
			nw_dict = {'Aucune_etape': "Une erreur sur les étapes lors de l'enregistrement de ces données ont été relevé"}
			error = True
		else:
			nw_dict= {'Aucune_etape': "Aucune étape enregistré dans les bases de données"}
			error = True

		return [error, nw_dict]
	else:
		etape_etude = dict_etape_value
		error = False

		return [error, etape_etude]

def etudeRecente(etude_recente,dossier_all):
	list_centre = []	
	if etude_recente.exists():
		for inf in dossier_all:
			item = RefInfocentre.objects.get(user__exact=inf.user.id)
			if item not in list_centre:
				list_centre.append(item)
	return list_centre

def etudeTris(dossier_all):
	list_centre = []	
	for inf in dossier_all:
		item = RefInfocentre.objects.get(user__exact=inf.user.id)
		if item not in list_centre:
			list_centre.append(item)
	return list_centre


def gestionEtudeRecente(etude_recente,dossier_all,list_centre):
	list_etude = RefEtudes.objects.all()
	list_infcentre = RefInfocentre.objects.all()
	str_etude = []
	str_centre = []
	str_dict = {}

	for centre in list_centre:

		str_dict_centre = {} 
		str_dict_centre['id'] = centre.id
		str_dict_centre['nom'] = str(centre.nom) + str(centre.numero)
		str_centre.append(str_dict_centre)

	for etude in list_etude:
		str_dict = {}

		if etude_recente.exists():
			var_id = etude_recente[0].etude.etude.id
		else:
			var_id = -1

		if etude.id == var_id:
			str_dict['id'] = str(etude.id)
			str_dict['option'] = 'selected'
			str_dict['nom'] = etude.nom
			str_etude.append(str_dict)
		else:
			str_dict['id'] = str(etude.id)
			str_dict['option'] = ''
			str_dict['nom'] = etude.nom
			str_etude.append(str_dict)
	return [str_centre,str_etude]

def gestionEtudeTris(etude_change,dossier_all,list_centre):
	list_etude = RefEtudes.objects.all()
	list_infcentre = RefInfocentre.objects.all()
	str_etude = []
	str_centre = []
	str_dict = {}

	for centre in list_centre:

		str_dict_centre = {} 
		str_dict_centre['id'] = centre.id
		str_dict_centre['nom'] = str(centre.nom) + str(centre.numero)
		str_centre.append(str_dict_centre)

	for etude in list_etude:
		str_dict = {}
		if etude.id == etude_change.id:
			str_dict['id'] = str(etude.id)
			str_dict['option'] = 'selected'
			str_dict['nom'] = etude.nom
			str_etude.append(str_dict)
		else:
			str_dict['id'] = str(etude.id)
			str_dict['option'] = ''
			str_dict['nom'] = etude.nom
			str_etude.append(str_dict)
	return [str_centre,str_etude]

def dictUpload(dict_upload,files):
	nbr_files = SuiviUpload.objects.filter(dossier__exact=files.dossier.id).count()
	name_etude = SuiviUpload.objects.filter(dossier__exact=files.dossier.id)[:1]
	var_qc = DossierUpload.objects.get(id__exact=name_etude[0].dossier.id)

	dict_upload['id_'] = files.id
	dict_upload['Etudes'] = var_qc.controle_qualite.nom
	dict_upload['Etudes_id'] = var_qc.id
	dict_upload['id'] = name_etude[0].id_patient
	dict_upload['nbr_upload'] = nbr_files

	return dict_upload

def infoEtape(files):
	etape = JonctionEtapeSuivi.objects.filter(upload__exact=files.dossier.id).order_by('etape')
	dict_etape_value = []

	for item in etape:
		if item.etat.id == 4:
			dict_etape_value.append({"val_item":item.date, "val_id":item.id, 'block':True})		
		else:
			dict_etape_value.append({"val_item":item.etat.nom, "val_id":item.id, 'block':False})
	return dict_etape_value

def nomEtape(etude_recente):
	nom_etape = RefEtapeEtude.objects.filter(etude__exact=etude_recente[0].id)
	dict_etape_nom = []

	for nom in nom_etape:
		dict_etape_nom.append(nom.nom)
	return dict_etape_nom

def nomEtapeTris(etude_change):
	nom_etape = RefEtapeEtude.objects.filter(etude__exact=etude_change.id)
	dict_etape_nom = []

	for nom in nom_etape:
		dict_etape_nom.append(nom.nom)
	return dict_etape_nom