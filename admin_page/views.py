from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import FormsEtude, FormsEtape, FormsAutorisation, FormsUser
from upload.models import RefEtudes, JonctionUtilisateurEtude, RefEtapeEtude

# Create your views here.
@login_required(login_url="/auth/auth_in/")
def adminpage(request):

	return render(request,
		'admin_page.html')

@login_required(login_url="/auth/auth_in/")
def adminetude(request):
	if request.method == 'POST':
		nom = request.POST['nom']
		date = request.POST['date']
		user_current = request.user

		RefEtudes.objects.create(nom=nom, date_ouverture=date)
	
	form = FormsEtude()
	etude_tab = RefEtudes.objects.all()
	return render(request,
		'admin_etude.html',{"form":form, 'resultat':etude_tab})

@login_required(login_url="/auth/auth_in/")
def adminetape(request):
	liste_protocole = []
	if request.method == 'POST':
		nom = request.POST['nom']
		etude = request.POST['etude']

		RefEtapeEtude.objects.create(nom=nom, etude=etude)

	form = FormsEtape()
	request_etude = RefEtudes.objects.all()

	for util_pro in enumerate(request_etude):

		collapse = util_pro
		liste_protocole.append(collapse)

	form.fields['etudes'].choices = liste_protocole

	etape_tab = RefEtapeEtude.objects.all()
	return render(request,
		'admin_etapes.html',{"form":form, 'resultat':etape_tab})

@login_required(login_url="/auth/auth_in/")
def etapeEdit(request, id_etape):
	liste_protocole = []

	if request.method == 'POST':
		form = FormsEtape()
		request_etude = RefEtudes.objects.all()

		for util_pro in enumerate(request_etude):

			collapse = util_pro
			liste_protocole.append(collapse)

		form.fields['etudes'].choices = liste_protocole
		print(id_etape)
		return HttpResponseRedirect('/admin_page/etapes/')
	else:
		etape_filtre = RefEtapeEtude.objects.get(id=id_etape)
		id_etude = RefEtudes.objects.get(nom=etape_filtre.etude)

		print(etape_filtre.nom)

		form = FormsEtape()
		request_etude = RefEtudes.objects.all()

		for util_pro in enumerate(request_etude):

			collapse = util_pro
			liste_protocole.append(collapse)

		#form = FormsEtape(default_data)
		field_choice = id_etude.id - 1
		form.fields['etudes'].choices = liste_protocole
		form.fields['etudes'].initial = [field_choice]
		form.fields['nom'].initial = etape_filtre.nom

	etape_tab = RefEtapeEtude.objects.all()
	return render(request,
		'admin_etapes_edit.html',{"form":form, 'resultat':etape_tab})