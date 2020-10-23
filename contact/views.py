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

from .forms import ContactForm
from upload.models import Contact, RefTypeAction, log

from datetime import date, time, datetime
# Create your views here.
@login_required(login_url="/auth/auth_in/")
def gestioncontact(request):
	form = ContactForm()
	contact_tab = Contact.objects.all()
	date_now = timezone.now()
	user_current = request.user
	type_action = RefTypeAction.objects.get(pk=4)
	log.objects.create(user=user_current, action=type_action, date=date_now, info="Visite des contacts")
	return render(request,'contact.html', {'resultat':contact_tab, 'form':form})

@login_required(login_url="/auth/auth_in/")
def newContact(request):
	if request.method == 'POST':
		form = ContactForm()
		nom = request.POST['nom']
		prenom = request.POST['prenom']
		courriel = request.POST['email']
		telephone = request.POST['telephone']
		poste = request.POST['poste']
		Contact.objects.create(nom=nom, prenom=prenom, courriel=courriel, telephone=telephone, poste=poste)
	return redirect('/contact/')
	

@login_required(login_url="/auth/auth_in/")
def contactEdit(request, id):
	if request.method == 'POST':
		form = ContactForm()
		nom = request.POST['nom']
		prenom = request.POST['prenom']
		courriel = request.POST['email']
		telephone = request.POST['telephone']
		poste = request.POST['poste']
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		date_now = timezone.now()
		user_current = request.user
		type_action = RefTypeAction.objects.get(pk=2)
		nom_documentaire = 'Edition du contact : ' + str(nom) + " " + str(prenom) + "id: " + str(id)
		log.objects.create(user=user_current, action=type_action, date=date_now, info=nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
		Contact.objects.filter(id=id).update(nom=nom, prenom=prenom, courriel=courriel, telephone=telephone, poste=poste)
		return redirect('/contact/')
	else:
		obj = Contact.objects.get(id__exact=id)
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		date_now = timezone.now()
		user_current = request.user
		type_action = RefTypeAction.objects.get(pk=2)
		nom_documentaire = "Affichage de l'édition du contact : " + str(obj.nom) + " " + str(obj.prenom)
		log.objects.create(user=user_current, action=type_action, date=date_now, info=nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
		info = {
			"nom": obj.nom,
			"prenom": obj.prenom,
			"email": obj.courriel,
			"telephone": obj.telephone,
			"poste": obj.poste,
		}
		form = ContactForm(info)
	contact_tab = Contact.objects.all()
	return render(request,
		'contact_edit.html',{"form":form, 'resultat':contact_tab, 'select':int(id)})

@login_required(login_url="/auth/auth_in/")
def contactDeleted(request, id):
	liste_protocole = []

	if request.method == 'POST':
		var_suivi = Contact.objects.get(id=int(id))
		#Enregistrement du log------------------------------------------------------------------------
		#---------------------------------------------------------------------------------------------
		date_now = timezone.now()
		user_current = request.user
		type_action = RefTypeAction.objects.get(pk=3)
		nom_documentaire = "Suppression du contact : " + str(var_suivi.nom) + " " + str(var_suivi.prenom)
		log.objects.create(user=user_current, action=type_action, date=date_now, info=nom_documentaire)
		#----------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------
		var_suivi.delete()
		message = messages.add_message(
			request,
			messages.WARNING,
			"Suppression Faite")
	form = ContactForm()
	contact_tab = Contact.objects.all()
	context = {"form":form, 'resultat':contact_tab, 'message':message}
	return render(request,'contact.html', context)
