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
