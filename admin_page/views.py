from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.db.models import Count, Q
import json

from datetime import date, time, datetime
from .module_admin import checkmdp, take_data, choiceEtude, choiceCentre

from .forms import FormsEtude, FormsEtape, FormsAutorisation, FormsUser, FormsUserEdit, FormCentre
from upload.models import RefEtudes, JonctionUtilisateurEtude, RefEtapeEtude, RefInfocentre, JonctionEtapeSuivi, SuiviUpload,DossierUpload

# Create your views here.
@login_required(login_url="/auth/auth_in/")
def adminpage(request):
	label_etude = []
	data_etude = []
	label_etude_final = []


	list_etude = RefEtudes.objects.all()
	for item in list_etude:
		label_etude.append(str(item.nom))
		#count_etude = Count('id', filter=Q(suiviupload__etude__exact=item.id))
		#nbr = DossierUpload.objects.annotate(count_etude=count_etude).distinct()
		nbr_img = SuiviUpload.objects.filter(etude__etude__exact=item.id)
		list_dossier = []
		x = 0
		for img in nbr_img:
			if not type(img.dossier.id) == None:
				if img.dossier.id not in list_dossier:
					list_dossier.append(img.dossier.id)
					x += 1
		data_etude.append(x)

	print(data_etude)
	
	return render(request,
		'admin_page.html', {"label_etude":json.dumps(label_etude), "data_etude":json.dumps(data_etude)})

# Gère la partie Admin Etudes
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
@login_required(login_url="/auth/auth_in/")
def adminetude(request):
	if request.method == 'POST':
		nom = request.POST['nom']

		user_current = request.user

		date_now = datetime.now()
		RefEtudes.objects.create(nom=nom, date_ouverture=date_now.date())
	
	form = FormsEtude()
	etude_tab = RefEtudes.objects.all()
	return render(request,
		'admin_etude.html',{"form":form, 'resultat':etude_tab})

@login_required(login_url="/auth/auth_in/")
def etudeEdit(request, id_etape):
	liste_protocole = []

	if request.method == 'POST':
		form = FormsEtude()

		nom = request.POST['nom']
		date = request.POST['date_ouverture']

		user_info = RefEtudes.objects.get(pk=id_etape)

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

	etude_tab = RefEtudes.objects.all().order_by('nom')
	return render(request,
		'admin_etude_edit.html',{"form":form, 'resultat':etude_tab, 'select':int(id_etape)})


@login_required(login_url="/auth/auth_in/")
def etudeDel(request, id_etape):
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

			RefEtudes.objects.get(id__exact=id_etape).delete()

			message = messages.add_message(
		        request,
		        messages.WARNING,
		        "Suppression Faite")

		else:
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
	liste_protocole = []
	if request.method == 'POST':
		val_nom = request.POST['nom']
		val_etude = request.POST['etudes']

		query = RefEtudes.objects.get(id__exact=val_etude)
		RefEtapeEtude.objects.create(nom=val_nom, etude=query)

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
	liste_protocole = []

	if request.method == 'POST':
		select_etape = RefEtapeEtude.objects.get(pk=id_etape)
		nom = request.POST['nom']
		etudes = request.POST['etudes']

		#nbr = int(etudes) + 1
		ref_etude = RefEtudes.objects.get(id=etudes)

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

	etape_tab = RefEtapeEtude.objects.all()
	return render(request,
		'admin_etapes_edit.html',{"form":form, 'resultat':etape_tab, 'select':int(id_etape)})

@login_required(login_url="/auth/auth_in/")
def etapeDel(request, id_etape):
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

			RefEtapeEtude.objects.get(id__exact=id_etape).delete()

			message = messages.add_message(
		        request,
		        messages.WARNING,
		        "Suppression Faite")

		else:
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
	liste_protocole = []
	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		nom = request.POST['nom']
		numero = request.POST['numero']
		pass_first = request.POST['pass_first']
		pass_second = request.POST['pass_second']


		check_mdp = checkmdp(pass_first, pass_second)

		if check_mdp :
			nw_user = User.objects.create_user(
			username=username, password=pass_first, email=email)
			nw_user.save()
			
			if len(nom) > 0 and len(numero) > 0:
				date_now = datetime.now()
				nw_centre = RefInfocentre(nom=nom, numero=numero, date_ajout=date_now.date())
				nw_centre.save()
				nw_centre.user.add(nw_user)

	form = FormsUser()
	user_tab = User.objects.all().order_by('username')
	return render(request,
		'admin_user.html',{"form":form, 'resultat':user_tab})

@login_required(login_url="/auth/auth_in/")
def userEdit(request, id_etape):
	liste_protocole = []

	if request.method == 'POST':
		form = FormsUserEdit()

		username = request.POST['username']
		email = request.POST['email']

		pass_first = request.POST['pass_first']
		pass_second = request.POST['pass_second']

		user_info = User.objects.get(pk=id_etape)

		check_mdp = checkmdp(pass_first, pass_second)

		if checkmdp:
			user_info.username = username
			user_info.email = email

			user_info.set_password(pass_first)

			user_info.save()
		else:
			user_info.username = username
			user_info.email = email

		return HttpResponseRedirect('/admin_page/viewUser/')
	else:
		user_info = User.objects.get(pk=id_etape)
		info = {
		'username': user_info.username,
		'email': user_info.email,
		}

		form = FormsUserEdit(info)

	user_tab = User.objects.all().order_by('username')

	return render(request,
		'admin_user_edit.html',{"form":form, 'resultat':user_tab, 'select':int(id_etape)})

@login_required(login_url="/auth/auth_in/")
def userDel(request, id_etape):
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
	liste_protocole = []
	if request.method == 'POST':
		nom = request.POST['nom']
		numero = request.POST['numero']
	
		date_now = datetime.now()
		nw_centre = RefInfocentre.objects.create(nom=nom, numero=numero, date_ajout=date_now.date())

	form = FormCentre()
	centre_tab = RefInfocentre.objects.all().order_by('nom')
	return render(request,
		'admin_centre.html',{"form":form, 'resultat':centre_tab})

@login_required(login_url="/auth/auth_in/")
def centreEdit(request, id_etape):
	liste_protocole = []

	if request.method == 'POST':
		form = FormCentre()

		nom = request.POST['nom']
		numero = request.POST['numero']

		user_info = RefInfocentre.objects.get(pk=id_etape)

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

	centre_tab = RefInfocentre.objects.all().order_by('nom')
	return render(request,
		'admin_centre_edit.html',{"form":form, 'resultat':centre_tab, 'select':int(id_etape)})

@login_required(login_url="/auth/auth_in/")
def centreDel(request, id_etape):
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

	form = FormCentre()

	centre_tab = RefInfocentre.objects.all().order_by('nom')
	context = {"form":form, 'resultat':centre_tab, 'message':message}
	return render(request,'admin_centre.html', context)

@login_required(login_url="/auth/auth_in/")
def adminauth(request):
	liste_protocole = []

	user_tab = User.objects.all().order_by('username')
	return render(request,
		'admin_autorisation.html',{'resultat':user_tab})

@login_required(login_url="/auth/auth_in/")
def authEdit(request, id_etape):
	liste_etude = []
	liste_centre = []

	user_info = User.objects.get(pk=id_etape)

	if request.method == 'POST':
		form = FormsAutorisation()

		etude = request.POST['etude']
		centre = request.POST['centre']

		user_centre = RefInfocentre.objects.filter(user__id__exact=id_etape).filter(id=centre)
		user_etude = JonctionUtilisateurEtude.objects.filter(user__exact=id_etape).filter(etude__id__exact=etude)

		if not user_etude.exists() and int(etude) > 0:
			date_now = datetime.now()
			save_etude = RefEtudes.objects.get(pk=etude)
			nw_jonction = JonctionUtilisateurEtude.objects.create(user=user_info, etude=save_etude, date_autorisation=date_now.date())

		if not user_centre.exists() and int(centre) > 0:
			date_now = datetime.now()
			save_centre = RefInfocentre.objects.get(pk=centre)
			save_centre.user.add(user_info)
		else:
			print("ne prend pas en compte")


	liste_etude = choiceEtude(True)
	liste_centre = choiceCentre(True)

	form = FormsAutorisation()

	form.fields['etude'].choices = liste_etude
	form.fields['etude'].initial = [0]
	form.fields['centre'].choices = liste_centre
	form.fields['centre'].initial = [0]

	user_centre = RefInfocentre.objects.filter(user__id__exact=id_etape)
	user_etude = JonctionUtilisateurEtude.objects.filter(user__exact=id_etape)

	#centre_tab = RefInfocentre.objects.all().order_by('nom')
	return render(request,
		'admin_auth_edit.html',{"form":form, 'etude':user_etude, 'centre':user_centre, 'user':user_info})

