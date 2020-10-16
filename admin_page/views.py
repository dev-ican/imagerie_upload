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

from .forms import FormsEtude, FormsEtape, FormsAutorisation, FormsUser, FormsUserEdit, FormCentre
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

# Permet d'afficher la page des étapes de chaque étude
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------

@login_required(login_url="/auth/auth_in/")
def adminup(request):
	''' Affiche la page du tableau gérant les différents état des étapes d'une étude. '''
	tab_list = []
	list_centre = []
	dict_upload = {}
	dict_nbr = {}
	etude_recente = SuiviUpload.objects.get(id=SuiviUpload.objects.all().order_by('dossier', 'date_upload')[:1])
	try:
		dossier_all = SuiviUpload.objects.filter(etude=etude_recente.etude).distinct('dossier')
		nbr_etape = RefEtapeEtude.objects.filter(etude=etude_recente.etude.etude).count()
		nom_etape = nomEtape(etude_recente)
		for files in dossier_all:
			dict_upload = {}
			dict_upload = dictUpload(dict_upload,files)
			info_etape = infoEtape(files)
			var_etape = gestionetape(nom_etape, info_etape,nbr_etape)
			if len(var_etape) == 2:
				dict_upload['etape_etude'] = var_etape[1] 
			dict_upload['error'] = var_etape[0]
			tab_list.append(dict_upload)
		dict_nbr['nbr_etape'] = nbr_etape
		dict_nbr['nom_etape'] = nom_etape
		list_centre = etudeRecente(etude_recente,dossier_all)
		gestion_info = gestionEtudeRecente(etude_recente, dossier_all,list_centre)
	except ObjectDoesNotExist:
		dossier_all = ""
		gestion_info = gestionEtudeRecente(etude_recente, dossier_all,list_centre)
	nbr_entrée = len(tab_list)
	#Enregistrement du log------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------------
	nom_documentaire = " Affiche le tableau des études en cours"
	informationLog(request, nom_documentaire)
	#----------------------------------------------------------------------------------------------
	#----------------------------------------------------------------------------------------------
	return render(request,
		'admin_page_upload.html', {'resultat':tab_list, 'dict_nbr':dict_nbr, 'str_etude':gestion_info[1], 'str_centre':gestion_info[0], 'taille':nbr_entrée})

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

@login_required(login_url="/auth/auth_in/")
def affdossier(request, id_suivi):
	''' Lors du clic sur un dossier chargé dans le tableau des étapes, cela appel le module qui affiche les fichiers
	chargé pour le patient donné'''
	tab_list = []
	var_suivi = SuiviUpload.objects.get(id__exact=id_suivi)
	list_lien = SuiviUpload.objects.filter(dossier__id__exact=var_suivi.dossier.id)
	for item in list_lien:
		dict_list = {}
		lien = str(item.fichiers)
		tab_lien = lien.split('/')
		nom = tab_lien[-1]
		dict_list = {'nom':nom, 'url':item.id}
		tab_list.append(dict_list)
	info_dossier = {"id":var_suivi.id_patient, "etude":var_suivi.etude.etude.nom, 'lien':var_suivi.id}
	#Enregistrement du log------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------------
	nom_documentaire = " a listé les informations du patient : " + var_suivi.id_patient
	informationLog(request, nom_documentaire)
	#----------------------------------------------------------------------------------------------
	#----------------------------------------------------------------------------------------------
	return render(request,
		'admin_page_down.html', {'resultat':tab_list, 'tab_dossier':info_dossier})

@login_required(login_url="/auth/auth_in/")
def downOnce(request, id):
	''' Ce module est appelé lors du téléchargement d'un fichier chargé pour le patient donnée '''
	obj = SuiviUpload.objects.get(id__exact=id)
	filename = obj.fichiers.path
	file_path = os.path.join(settings.MEDIA_ROOT, filename)
	if os.path.exists(file_path):
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		nom_documentaire = " a téléchargé le document : " + file_path
		informationLog(request, nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response

@login_required(login_url="/auth/auth_in/")
def downAll(request, id):
	''' Ce module est appelé lorsque l'utilisateur souhaite téléchargé la totalité des fichiers chargé dans le dossier
	Ce téléchargement utilise zipfile en mémoir temporaire '''
	obj = SuiviUpload.objects.get(id__exact=id)
	list_lien = SuiviUpload.objects.filter(dossier__id__exact=obj.dossier.id)
	in_memory = BytesIO()
	zip = zipfile.ZipFile(in_memory, "a")
	for item in list_lien:
		lien = str(item.fichiers)
		tab_lien = lien.split('/')
		nom = tab_lien[-1]
		del tab_lien[-1]
		file_path = os.path.join(settings.MEDIA_ROOT, lien)
		img = open(file_path, "rb") #changer avec with
		img_read = img.read()
		zip.writestr(nom, img_read)
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

# Gère la partie Admin Etudes
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
@login_required(login_url="/auth/auth_in/")
def adminetude(request):
	''' Charge la page index pour l'ajout ou l'édition d'une étude '''
	if request.method == 'POST':
		nom = request.POST['nom']
		user_current = request.user
		date_now = timezone.now()
		RefEtudes.objects.create(nom=nom, date_ouverture=date_now)
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		nom_documentaire = " a créé l'étude : " + nom
		creationLog(request, nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
	form = FormsEtude()
	etude_tab = RefEtudes.objects.all()
	return render(request,
		'admin_etude.html',{"form":form, 'resultat':etude_tab})

@login_required(login_url="/auth/auth_in/")
def etudeEdit(request, id_etape):
	''' Charge la page d'édition des études '''
	liste_protocole = []
	if request.method == 'POST':
		form = FormsEtude()
		nom = request.POST['nom']
		date = request.POST['date_ouverture']
		user_info = RefEtudes.objects.get(pk=id_etape)
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		nom_documentaire = " a editer l'étude id/nom/nouveau nom : " + id_etape + "/" + user_info.nom + "/" + nom
		editionLog(request, nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
		user_info.nom = nom
		user_info.date_ouverture = date
		user_info.save()
		return HttpResponseRedirect('/admin_page/etudes/')
	else:
		user_info = RefEtudes.objects.get(pk=id_etape)
		info = {
		'nom': user_info.nom,
		'date': user_info.date_ouverture
		}
		form = FormsEtude(info)
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		nom_documentaire = " a ouvert l'édition pour l'étude id/nouveau nom : " + id_etape + "/" + user_info.nom
		informationLog(request, nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
	etude_tab = RefEtudes.objects.all().order_by('nom')
	return render(request,
		'admin_etude_edit.html',{"form":form, 'resultat':etude_tab, 'select':int(id_etape)})


@login_required(login_url="/auth/auth_in/")
def etudeDel(request, id_etape):
	''' Appel Ajax permettant la supression d'une étude '''
	liste_protocole = []
	x = 0
	if request.method == 'POST':
		info_etape = RefEtapeEtude.objects.filter(etude__id__exact=id_etape)
		if info_etape.exists():
			for item in info_etape:
				info_suivi = JonctionEtapeSuivi.objects.filter(etape__exact=item.id)
				if info_suivi.exists():
					x += 1
					suppr = False
			if x == 0:
				suppr = True
		else:
			suppr = True
		if suppr == True:
			id_log = RefEtudes.objects.get(id__exact=id_etape)
			#Enregistrement du log------------------------------------------------------------------------
			#---------------------------------------------------------------------------------------------
			nom_documentaire = " a supprimé l'étude (id/nom) : " + id_log.id + "/" + id_log.nom
			supprLog(request, nom_documentaire)
			#----------------------------------------------------------------------------------------------
			#---------------------------------------------------------------------------------------------
			RefEtudes.objects.get(id__exact=id_etape).delete()
			message = messages.add_message(
				request,
				messages.WARNING,
				"Suppression Faite")
		else:
			id_log = RefEtudes.objects.get(id__exact=id_etape)
			#Enregistrement du log------------------------------------------------------------------------
			#---------------------------------------------------------------------------------------------
			nom_documentaire = " a reçu un message d'erreur de suppression pour (id/nom) : " + id_log.id + "/" + id_log.nom
			informationLog(request, nom_documentaire)
			#----------------------------------------------------------------------------------------------
			#---------------------------------------------------------------------------------------------
			message = messages.add_message(
				request,
				messages.WARNING,
				"Suppression annulée, cette étude est liée à :" + x + " suivi(s)")
	form = FormsEtude()
	etude_tab = RefEtudes.objects.all().order_by('nom')
	context = {"form":form, 'resultat':etude_tab, 'message':message}
	return render(request,'admin_etude.html', context)

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


# Gère la partie Admin Utilisateur
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------


@login_required(login_url="/auth/auth_in/")
def adminuser(request):
	''' Charge la page index pour l'ajout ou l'édition d'un utilisateur '''
	liste_protocole = []
	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		nom = request.POST['nom']
		numero = request.POST['numero']
		pass_first = request.POST['pass_first']
		pass_second = request.POST['pass_second']
		type = request.POST['type']
		check_mdp = checkmdp(pass_first, pass_second)
		nwPassword(check_mdp, type, nom, numero, username, pass_first, email)
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		nom_documentaire = " a créé l'utilisateur : " + username
		creationLog(request, nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
	form = FormsUser()
	user_tab = User.objects.all().order_by('username')
	return render(request,
		'admin_user.html',{"form":form, 'resultat':user_tab})

@login_required(login_url="/auth/auth_in/")
def userEdit(request, id_etape):
	''' Charge la page d'édition des utilisateurs '''
	liste_protocole = []
	if request.method == 'POST':
		form = FormsUserEdit()
		type = request.POST['type']
		username = request.POST['username']
		email = request.POST['email']
		pass_first = request.POST['pass_first']
		pass_second = request.POST['pass_second']
		user_info = User.objects.get(pk=id_etape)
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		nom_documentaire =  " a editer l'utilisateur (id): " + user_info.username + ' (' + user_info.id + ')'
		editionLog(request, nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
		check_mdp = checkmdp(pass_first, pass_second)
		editPassword(check_mdp, type, username, pass_first, email, user_info)
		return HttpResponseRedirect('/admin_page/viewUser/')
	else:
		user_info = User.objects.get(pk=id_etape)
		info = {
		'username': user_info.username,
		'email': user_info.email,
		}
		form = FormsUserEdit(info)
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		nom_documentaire = " a ouvert l'édition pour l'utilisateur : " + user_info.username
		informationLog(request, nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
	user_tab = User.objects.all().order_by('username')
	return render(request,
		'admin_user_edit.html',{"form":form, 'resultat':user_tab, 'select':int(id_etape)})

@login_required(login_url="/auth/auth_in/")
def userDel(request, id_etape):
	''' Appel Ajax permettant la supression d'un utilisateur '''
	liste_protocole = []
	x = 0
	if request.method == 'POST':
		suppr = True
		info_suivi = User.objects.get(id__exact=id_etape)
		info_upload =  SuiviUpload.objects.filter(user__id__exact=info_suivi.id)
		if info_upload.exists():
			for nbr in info_upload:
				x += 1
			suppr = False
		if suppr == True:
			#Enregistrement du log------------------------------------------------------------------------
			#---------------------------------------------------------------------------------------------
			nom_documentaire = " a supprimé l'utilisateur : " + info_suivi.username
			supprLog(request, nom_documentaire)
			#----------------------------------------------------------------------------------------------
			#---------------------------------------------------------------------------------------------
			exist_jonction = JonctionUtilisateurEtude.objects.filter(user__id__exact=info_suivi.id)
			if exist_jonction.exists():
				JonctionUtilisateurEtude.objects.get(user__exact=info_suivi).delete()
			User.objects.get(id__exact=id_etape).delete()
			message = messages.add_message(
				request,
				messages.WARNING,
				"Suppression Faite")
		else:
			if x == 0 :
				terme = "suivi"
			else:
				terme = "suivis"
			message = messages.add_message(
				request,
				messages.WARNING,
				"Suppression annulée, cette étape est liée à : " + str(x) + terme)
			#Enregistrement du log------------------------------------------------------------------------
			#---------------------------------------------------------------------------------------------
			nom_documentaire = " à reçu un message d'erreur de suppression pour l'utilisateur : " + info_suivi.username
			informationLog(request, nom_documentaire)
			#----------------------------------------------------------------------------------------------
			#---------------------------------------------------------------------------------------------
	form = FormsUser()
	user_tab = User.objects.all().order_by('username')
	context = {"form":form, 'resultat':user_tab, 'message':message}
	return render(request,'admin_user.html', context)


# Gère la partie Admin Centres
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------


@login_required(login_url="/auth/auth_in/")
def admincentre(request):
	''' Charge la page index pour l'ajout ou l'édition d'un centre '''
	liste_protocole = []
	if request.method == 'POST':
		nom = request.POST['nom']
		numero = request.POST['numero']
		date_now = timezone.now()
		nw_centre = RefInfocentre.objects.create(nom=nom, numero=numero, date_ajout=date_now)
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		nom_documentaire = " a créé le centre : " + nw_centre.nom + nw_centre.numero
		creationLog(request, nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
	form = FormCentre()
	centre_tab = RefInfocentre.objects.all().order_by('nom')
	return render(request,
		'admin_centre.html',{"form":form, 'resultat':centre_tab})

@login_required(login_url="/auth/auth_in/")
def centreEdit(request, id_etape):
	''' Charge la page d'édition des centres '''
	liste_protocole = []
	if request.method == 'POST':
		form = FormCentre()
		nom = request.POST['nom']
		numero = request.POST['numero']
		user_info = RefInfocentre.objects.get(pk=id_etape)
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		nom_documentaire =  " a editer le centre : " + user_info.nom + user_info.numero + ' (Nouvelle entrée : ' + nom + numero + ')'
		editionLog(request, nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
		user_info.nom = nom
		user_info.numero = numero
		user_info.save()
		return HttpResponseRedirect('/admin_page/centre/')
	else:
		user_info = RefInfocentre.objects.get(pk=id_etape)
		info = {
		'nom': user_info.nom,
		'numero': user_info.numero,
		'date_ajout': user_info.date_ajout
		}
		form = FormCentre(info)
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		nom_documentaire = " a ouvert l'édition pour le centre : " + user_info.nom + user_info.numero
		informationLog(request, nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
	centre_tab = RefInfocentre.objects.all().order_by('nom')
	return render(request,
		'admin_centre_edit.html',{"form":form, 'resultat':centre_tab, 'select':int(id_etape)})

@login_required(login_url="/auth/auth_in/")
def centreDel(request, id_etape):
	''' Appel Ajax permettant la supression d'un centre '''
	liste_protocole = []
	x = 0
	if request.method == 'POST':
		suppr = True
		info_centre = RefInfocentre.objects.get(id__exact=id_etape)
		info_user = User.objects.filter(refinfocentre__id__exact=info_centre.id)
		if info_user.exists():
			for item in info_user:
				info_suivi = SuiviUpload.objects.filter(user__exact=item.id)
				if info_suivi.exists():
					for nbr in info_suivi:
						x += 1
					suppr = False
		if suppr == True:
			#Enregistrement du log------------------------------------------------------------------------
			#---------------------------------------------------------------------------------------------
			nom_documentaire = " a supprimé le centre : " + info_centre.nom + info_centre.numero
			supprLog(request, nom_documentaire)
			#----------------------------------------------------------------------------------------------
			#---------------------------------------------------------------------------------------------
			RefInfocentre.objects.get(id__exact=id_etape).delete()
			message = messages.add_message(
				request,
				messages.WARNING,
				"Suppression Faite")
		else:
			message = messages.add_message(
				request,
				messages.WARNING,
				"Suppression annulée, cette étape est liée à :" + x + " suivi(s)")
			#Enregistrement du log------------------------------------------------------------------------
			#---------------------------------------------------------------------------------------------
			nom_documentaire = " à reçu un message d'erreur de suppression pour le centre : " + info_centre.nom + info_centre.numero
			informationLog(request, nom_documentaire)
			#----------------------------------------------------------------------------------------------
			#---------------------------------------------------------------------------------------------
	form = FormCentre()
	centre_tab = RefInfocentre.objects.all().order_by('nom')
	context = {"form":form, 'resultat':centre_tab, 'message':message}
	return render(request,'admin_centre.html', context)

# Gère la partie autorisation
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------

@login_required(login_url="/auth/auth_in/")
def adminauth(request):
	''' Charge la page index pour l'autorisation des utilisateurs '''
	liste_protocole = []
	user_tab = User.objects.all().order_by('username')
	return render(request,
		'admin_autorisation.html',{'resultat':user_tab})


@login_required(login_url="/auth/auth_in/")
def authEdit(request, id_etape):
	''' Charge la page d'édition des autorisations utilisateur '''
	liste_etude = []
	liste_centre = []
	user_info = User.objects.get(pk=id_etape)
	if request.method == 'POST':
		form = FormsAutorisation()
		etude = request.POST['etude']
		centre = request.POST['centre']
		user_centre = RefInfocentre.objects.filter(user__id__exact=id_etape).filter(id=centre)
		user_etude = JonctionUtilisateurEtude.objects.filter(user__exact=id_etape).filter(etude__id__exact=etude)
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		nom_documentaire =  " a editer les autorisation de l'utilisateur : " + user_info.username 
		editionLog(request, nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
		joncCentre(user_etude, etude, user_info, user_centre, centre)
	liste_etude = choiceEtude(True)
	liste_centre = choiceCentre(True)
	form = FormsAutorisation()
	form.fields['etude'].choices = liste_etude
	form.fields['etude'].initial = [0]
	form.fields['centre'].choices = liste_centre
	form.fields['centre'].initial = [0]
	user_centre = RefInfocentre.objects.filter(user__id__exact=id_etape)
	user_etude = JonctionUtilisateurEtude.objects.filter(user__exact=id_etape)
	return render(request,
		'admin_auth_edit.html',{"form":form, 'etude':user_etude, 'centre':user_centre, 'user':user_info})

@login_required(login_url="/auth/auth_in/")
def authDel(request):
	''' Appel Ajax permettant la supression d'une autorisation '''
	liste_etude = []
	liste_centre = []
	id_user = request.POST.get('val_user')
	id_search = request.POST.get('val_id')
	type_tab = request.POST.get('type_tab')
	user_info = User.objects.get(pk=id_user)
	if request.method == 'POST':
		form = FormsAutorisation()
		message = delAuth(type_tab, id_search, request)
	user_centre = RefInfocentre.objects.filter(user__id__exact=user_info.id)
	user_etude = JonctionUtilisateurEtude.objects.filter(user__exact=user_info.id)
	var_etude = {}
	var_centre = {}
	x = 0
	for item in user_etude:
		date_j = j_serial(item.etude.date_ouverture)
		var_etude[x] = {'nom':item.etude.nom, 'date':date_j, 'type':'etude', 'id_jonc':item.id, 'id_user':user_info.id}
		x += 1
	x = 0
	for item in user_centre:
		date_j = j_serial(item.date_ajout)
		var_centre[x] = {'nom':item.nom, 'num':item.numero, 'date':date_j, 'type':'centre', 'id_jonc':item.id, 'id_user':user_info.id}
		x += 1
	context = {'etude':var_etude, 'centre':var_centre, 'message':message}
	creation_json = json.dumps(context)
	return HttpResponse(json.dumps(creation_json), content_type="application/json")



