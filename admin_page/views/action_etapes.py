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

@login_required(login_url="/auth/auth_in/")
def uploadtris(request, id_tris):
	''' Cette page est appelé lors du tris du tableau vers une autre étude, cet appel ce fait via ajax '''
	tab_list = []
	dict_nbr = {}
	etude_change = RefEtudes.objects.get(id=id_tris)
	dossier_all = SuiviUpload.objects.filter(etude__etude=id_tris).distinct('dossier')
	if dossier_all.exists():
		nbr_etape = RefEtapeEtude.objects.filter(etude=etude_change.id).count()
		nom_etape = nomEtapeTris(etude_change)
		for files in dossier_all:
			dict_upload = {}
			dict_upload = dictUpload(dict_upload,files)
			info_etape = infoEtape(files)
			var_etape = gestionetape(nom_etape, info_etape,nbr_etape)
			dict_upload['etape_etude'] = var_etape[1] 
			dict_upload['error'] = var_etape[0]
			tab_list.append(dict_upload)
		dict_nbr['nbr_etape'] = nbr_etape
		dict_nbr['nom_etape'] = nom_etape
	list_centre = etudeTris(dossier_all)
	gestion_info = gestionEtudeTris(etude_change, dossier_all,list_centre)
	nbr_entrée = len(tab_list)
	#Enregistrement du log------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------------
	nom_documentaire = " a créé un tris vers l'étude : " + etude_change.nom
	informationLog(request, nom_documentaire)
	#----------------------------------------------------------------------------------------------
	#----------------------------------------------------------------------------------------------
	return render(request,
		'admin_page_upload.html', {'resultat':tab_list, 'dict_nbr':dict_nbr, 'str_etude':gestion_info[1], 'str_centre':gestion_info[0], 'taille':nbr_entrée})

@xframe_options_exempt
@login_required(login_url="/auth/auth_in/")
def uploadmod(request):
	''' Appel ajax lors du double clic sur une case du tableau.
	Ce module renvois la liste des états d'une étape et l'intégre dans la cellule ou l'utilisateur à cliqué'''
	tab_list = {}
	val_etat = RefEtatEtape.objects.all()
	x = 0
	for etat in val_etat:
		var_str = 'etat_' + str(x)
		tab_list[var_str] = {'id':etat.id, 'nom':etat.nom, 'var':var_str}
		x += 1
	creation_json = json.dumps(tab_list)
	return HttpResponse(json.dumps(creation_json), content_type="application/json")

@xframe_options_exempt
@login_required(login_url="/auth/auth_in/")
def uploadmodqc(request):
	''' Appel ajax lors du double clic sur une case du tableau.
	Ce module renvois la liste des états du controle qualité et l'intégre dans la cellule ou l'utilisateur à cliqué'''
	tab_list = {}
	val_etat = RefControleQualite.objects.all()
	x = 0
	for etat in val_etat:
		var_str = 'etat_' + str(x)
		tab_list[var_str] = {'id':etat.id, 'nom':etat.nom}
		x += 1
	creation_json = json.dumps(tab_list)
	return HttpResponse(json.dumps(creation_json), content_type="application/json")

@xframe_options_exempt
@login_required(login_url="/auth/auth_in/")
def uploadmaj(request):
	''' Appel ajax lors du changement d'état d'une étape.
	Ce module modifie l'état dans la base de donnée puis renvois vers la page pour afficher la modification'''
	tab_list = {}
	val_jonction = request.GET.get('jonction')
	val_etat = request.GET.get('etat_id')
	val_etude = request.GET.get('etude_id')
	id_log = JonctionEtapeSuivi.objects.get(id__exact=val_jonction)
	if val_etat == str(4):
		date_now = datetime.today()
		JonctionEtapeSuivi.objects.filter(id__exact=val_jonction).update(etat=val_etat)
		JonctionEtapeSuivi.objects.filter(id__exact=val_jonction).update(date=date_now)
	else:
		JonctionEtapeSuivi.objects.filter(id__exact=val_jonction).update(etat=val_etat)
	var_url = '/admin_page/upfiles/tris/' + str(val_etude) + '/'
	#Enregistrement du log------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------------
	nom_documentaire = " a modifié l'état de l'étude : " + id_log.etape.etude.nom + " la nouvelle étape est : " + id_log.etat.nom
	editionLog(request, nom_documentaire)
	#----------------------------------------------------------------------------------------------
	#----------------------------------------------------------------------------------------------
	return redirect(var_url)

@xframe_options_exempt
@login_required(login_url="/auth/auth_in/")
def uploadmajqc(request):
	''' Appel ajax lors du changement d'état d'un controle qualité.
	Ce module modifie l'état dans la base de donnée puis renvois vers la page pour afficher la modification'''
	tab_list = {}
	val_jonction = request.GET.get('jonction')
	val_etat = request.GET.get('etat_id')
	val_etude = request.GET.get('etude_id')
	id_log = SuiviUpload.objects.filter(dossier__id__exact=val_jonction)[:1]
	qc = RefControleQualite.objects.get(id__exact=val_etat)
	DossierUpload.objects.filter(id__exact=val_jonction).update(controle_qualite=qc)
	var_url = '/admin_page/upfiles/tris/' + str(val_etude) + '/'
	#Enregistrement du log------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------------
	nom_documentaire = " a modifié l'état du controle qualité pour : " + id_log[0].id_patient + " la nouvelle étape est : " + qc.nom
	editionLog(request, nom_documentaire)
	#----------------------------------------------------------------------------------------------
	#----------------------------------------------------------------------------------------------
	return redirect(var_url)

@xframe_options_exempt
@login_required(login_url="/auth/auth_in/")
def walkup(request):
	''' Appel ajax lors du changement d'état d'un controle qualité.
	Ce module modifie l'état dans la base de donnée puis renvois vers la page pour afficher la modification'''
	tab_list = {}
	list_tr = []
	val_url = request.GET.get('url')
	val_etude = request.GET.get('etude_id')
	list_dir = os.listdir(val_url)
	for item in list_dir:
		lien_id = os.path.join(val_url, item)
		dict_list = {}
		if os.path.isdir(lien_id):
			for root, dirs, files in os.walk(lien_id, topdown = False):
				x = 0
				y = 0
				for name in files:
					x += 1
				for name in dirs:
					y += 1
			tab_list = {'nom':item, 'url':lien_id, 'dir': True, 'file':x, 'direct':y}
		else:
			dict_list = {'nom':item, 'url':lien_id, 'dir': False}
		list_tr.append(dict_list)

	creation_json = json.dumps(list_tr)
	#return render(request, 'admin_page_down.html', { 'value': list_tr, }, content_type='application/xhtml+xml')
	return HttpResponse(json.dumps(creation_json), content_type="application/json")

@login_required(login_url="/auth/auth_in/")
def walkdown(request):
	''' Appel ajax lors du changement d'état d'un controle qualité.
	Ce module modifie l'état dans la base de donnée puis renvois vers la page pour afficher la modification'''
	tab_list = {}
	list_tr = []
	val_url = request.GET.get('url')
	val_compare = request.GET.get('val_compare')
	val_etude_id = request.GET.get('id_etude')
	path = os.path.dirname(val_url)
	split_path = path.split('\\')
	del split_path[-1]
	path_join = '\\'.join(split_path)
	nom_folder = split_path[-1]
	if val_compare in path_join :
		list_dir = os.listdir(path_join)
		print(list_dir)
		for item in list_dir:
			lien_id = os.path.join(path_join, item)
			dict_list = {}
			if os.path.isdir(lien_id):
				for root, dirs, files in os.walk(lien_id, topdown = False):
					x = 0
					y = 0
					for name in files:
						x += 1
					for name in dirs:
						y += 1
				dict_list = {'nom':item, 'url':lien_id, 'dir': True, 'file':x, 'direct':y}
			else:
				dict_list = {'nom':item, 'url':lien_id, 'dir': False}
			list_tr.append(dict_list)
		creation_json = json.dumps(list_tr)
		return HttpResponse(json.dumps(creation_json), content_type="application/json")
	else:
		return HttpResponse()

@login_required(login_url="/auth/auth_in/")
def downOnce(request, id):
	''' Ce module est appelé lors du téléchargement d'un fichier chargé pour le patient donnée '''
	if os.path.exists(id):
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		nom_documentaire = " a téléchargé le document : " + id
		informationLog(request, nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
		with open(id, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(id)
			return response

@login_required(login_url="/auth/auth_in/")
def downAll(request, id):
	''' Ce module est appelé lorsque l'utilisateur souhaite téléchargé la totalité des fichiers chargé dans le dossier
	Ce téléchargement utilise zipfile en mémoir temporaire '''
	obj = SuiviUpload.objects.get(id__exact=id)
	path = os.path.dirname(obj.fichiers.path)
	list_dir = os.listdir(path)
	in_memory = BytesIO()
	zip = zipfile.ZipFile(in_memory, "a")
	for item in list_dir:
		file_path = os.path.join(path, item)
		print(file_path)
		img = open(file_path, "rb") #changer avec with
		img_read = img.read()
		zip.writestr(item, img_read)
	zip.close()
	response = HttpResponse(content_type='application/zip')
	response["Content-Disposition"] = "attachement;filename=corelab.zip"
	in_memory.seek(0)
	response.write(in_memory.read())
	#Enregistrement du log------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------------
	nom_documentaire = " a téléchargé tous les documents du patient : " + list_lien[0].id_patient
	informationLog(request, nom_documentaire)
	#----------------------------------------------------------------------------------------------
	#----------------------------------------------------------------------------------------------
	return response
