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

# Create your views here.
@login_required(login_url="/auth/auth_in/")
def adminpage(request):
	label_etude_final = []
	dict_etat = {}
	list_etude = RefEtudes.objects.all()
	#Nbr de patient dans un état donnée
	list_etat = RefEtatEtape.objects.all()
	for etude in list_etude:
		exist_etude = SuiviUpload.objects.filter(etude__etude__exact=etude.id).distinct('dossier')
		nbr_inclusion = SuiviUpload.objects.filter(etude__etude__exact=etude.id).distinct('dossier').count()	

		resume_etat = {}
		resume_etat['data'] = json.dumps({'nbr':[nbr_inclusion],'nom':[etude.nom]})
		if exist_etude.exists():

			for etat in list_etat:
				nbr_qc_ok = 0
				nbr_qc_not = 0
				nbr_qc_nw = 0
				for dossier in exist_etude:
					qc_dossier = DossierUpload.objects.get(id__exact=dossier.dossier.id)
					if DossierUpload.objects.filter(id__exact=dossier.dossier.id).exists():
						if qc_dossier.controle_qualite.id == 1:
							nbr_qc_nw += 1
						elif qc_dossier.controle_qualite.id == 2:
							nbr_qc_ok += 1
						elif qc_dossier.controle_qualite.id == 3:
							nbr_qc_not += 1
					nbr_etat = JonctionEtapeSuivi.objects.filter(upload__exact=dossier.dossier).filter(etat__exact=etat).count()
					resume_etat[etat.nom] = nbr_etat
			resume_etat['Nouveau'] = nbr_qc_nw
			resume_etat['Refused'] = nbr_qc_not
			resume_etat['Passed'] = nbr_qc_ok
			dict_etat[etude.nom] = resume_etat

	return render(request,
		'admin_page.html', {"nbr_etat":dict_etat})


@login_required(login_url="/auth/auth_in/")
def adminup(request):
	tab_list = []
	dict_upload = {}
	dict_nbr = {}

	etude_recente = SuiviUpload.objects.all().order_by('date_upload')[:1]

	if SuiviUpload.objects.all().order_by('date_upload')[:1].exists():
		dossier_all = SuiviUpload.objects.filter(etude__etude__exact=etude_recente[0].etude.etude.id).distinct('dossier')
		nbr_etape = RefEtapeEtude.objects.filter(etude__exact=etude_recente[0].id).count()
		nom_etape = RefEtapeEtude.objects.filter(etude__exact=etude_recente[0].id)
		dict_etape_nom = []

		for nom in nom_etape:
			dict_etape_nom.append(nom.nom)

		for files in dossier_all:
			nbr_files = SuiviUpload.objects.filter(dossier__exact=files.dossier.id).count()
			name_etude = SuiviUpload.objects.filter(dossier__exact=files.dossier.id)[:1]
			var_qc = DossierUpload.objects.get(id__exact=name_etude[0].dossier.id)

			dict_upload['id_'] = files.id
			dict_upload['Etudes'] = var_qc.controle_qualite.nom
			dict_upload['Etudes_id'] = var_qc.id
			dict_upload['id'] = name_etude[0].id_patient
			dict_upload['nbr_upload'] = nbr_files

			etape = JonctionEtapeSuivi.objects.filter(upload__exact=files.dossier.id).order_by('etape')
			dict_etape_value = []

			for item in etape:
				if item.etat.id == 4:
					dict_etape_value.append({"val_item":item.date, "val_id":item.id, 'block':True})		
				else:
					dict_etape_value.append({"val_item":item.etat.nom, "val_id":item.id, 'block':False})

			if len(dict_etape_nom) == 0 or len(dict_etape_value) != nbr_etape:
				if len(dict_etape_value) != nbr_etape:
					nw_dict = {'Aucune_etape': "Une erreur sur les étapes lors de l'enregistrement de ces données ont été relevé"}
					dict_upload['etape_etude'] = nw_dict
					dict_upload['error'] = True
				else:
					nw_dict= {'Aucune_etape': "Aucune étape enregistré dans les bases de données"}
					dict_upload['etape_etude'] = nw_dict
					dict_upload['error'] = True
			else:
				dict_upload['etape_etude'] = dict_etape_value
				dict_upload['error'] = False

			tab_list.append(dict_upload)
		dict_nbr['nbr_etape'] = nbr_etape
		dict_nbr['nom_etape'] = dict_etape_nom

	list_etude = RefEtudes.objects.all()
	list_infcentre = RefInfocentre.objects.all()
	list_centre = []

	if etude_recente.exists():
		for inf in dossier_all:
			item = RefInfocentre.objects.get(user__exact=inf.user.id)
			if item not in list_centre:
				list_centre.append(item)		

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

	nbr_entrée = len(tab_list)
	print(nbr_entrée)
	return render(request,
		'admin_page_upload.html', {'resultat':tab_list, 'dict_nbr':dict_nbr, 'str_etude':str_etude, 'str_centre':str_centre, 'taille':nbr_entrée})

@login_required(login_url="/auth/auth_in/")
def uploadtris(request, id_tris):
	tab_list = []
	dict_upload = {}
	dict_nbr = {}


	etude_change = RefEtudes.objects.get(id__exact=id_tris)
	dossier_all = SuiviUpload.objects.filter(etude__etude__exact=id_tris).distinct('dossier')

	if dossier_all.exists():
		nbr_etape = RefEtapeEtude.objects.filter(etude__exact=etude_change.id).count()
		nom_etape = RefEtapeEtude.objects.filter(etude__exact=etude_change.id)
		dict_etape_nom = []

		for nom in nom_etape:
			dict_etape_nom.append(nom.nom)

		for files in dossier_all:
			dict_upload = {}
			nbr_files = SuiviUpload.objects.filter(dossier__exact=files.dossier.id).count()
			name_etude = SuiviUpload.objects.filter(dossier__exact=files.dossier.id)[:1]
			var_qc = DossierUpload.objects.get(id__exact=name_etude[0].dossier.id)

			dict_upload['id_'] = files.id
			dict_upload['Etudes'] = var_qc.controle_qualite.nom
			dict_upload['Etudes_id'] = var_qc.id
			dict_upload['id'] = name_etude[0].id_patient
			dict_upload['nbr_upload'] = nbr_files

			etape = JonctionEtapeSuivi.objects.filter(upload__exact=files.dossier.id).order_by('etape')
			dict_etape_value = []
			
			for item in etape:
				if item.etat.id == 4:
					dict_etape_value.append({"val_item":item.date, "val_id":item.id, 'block':True})		
				else:
					dict_etape_value.append({"val_item":item.etat.nom, "val_id":item.id, 'block':False})

			if len(dict_etape_nom) == 0 or len(dict_etape_value) != nbr_etape:
				if len(dict_etape_value) != nbr_etape:
					nw_dict = {'Aucune_etape': "Une erreur sur les étapes lors de l'enregistrement de ces données ont été relevé"}
					dict_upload['etape_etude'] = nw_dict
					dict_upload['error'] = True
				else:
					nw_dict= {'Aucune_etape': "Aucune étape enregistré dans les bases de données"}
					dict_upload['etape_etude'] = nw_dict
					dict_upload['error'] = True
			else:
				dict_upload['etape_etude'] = dict_etape_value
				dict_upload['error'] = False

			tab_list.append(dict_upload)
		dict_nbr['nbr_etape'] = nbr_etape
		dict_nbr['nom_etape'] = dict_etape_nom

	list_etude = RefEtudes.objects.all()
	list_infcentre = RefInfocentre.objects.all()
	list_centre = []

	for inf in dossier_all:
		item = RefInfocentre.objects.get(user__exact=inf.user.id)
		if item not in list_centre:
			list_centre.append(item)

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

	nbr_entrée = len(tab_list)
	return render(request,
		'admin_page_upload.html', {'resultat':tab_list, 'dict_nbr':dict_nbr, 'str_etude':str_etude, 'str_centre':str_centre, 'taille':nbr_entrée})

@xframe_options_exempt
@login_required(login_url="/auth/auth_in/")
def uploadmod(request):
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
	tab_list = {}

	val_jonction = request.GET.get('jonction')
	val_etat = request.GET.get('etat_id')
	val_etude = request.GET.get('etude_id')

	print(val_etat)
	if val_etat == str(4):
		date_now = datetime.today()
		print(date_now)
		JonctionEtapeSuivi.objects.filter(id__exact=val_jonction).update(etat=val_etat)
		JonctionEtapeSuivi.objects.filter(id__exact=val_jonction).update(date=date_now)
	else:
		JonctionEtapeSuivi.objects.filter(id__exact=val_jonction).update(etat=val_etat)

	var_url = '/admin_page/upfiles/tris/' + str(val_etude) + '/'
	return redirect(var_url)

@xframe_options_exempt
@login_required(login_url="/auth/auth_in/")
def uploadmajqc(request):
	tab_list = {}

	val_jonction = request.GET.get('jonction')
	val_etat = request.GET.get('etat_id')
	val_etude = request.GET.get('etude_id')

	qc = RefControleQualite.objects.get(id__exact=val_etat)
	DossierUpload.objects.filter(id__exact=val_jonction).update(controle_qualite=qc)


	var_url = '/admin_page/upfiles/tris/' + str(val_etude) + '/'
	return redirect(var_url)

@login_required(login_url="/auth/auth_in/")
def affdossier(request, id_suivi):
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

	return render(request,
		'admin_page_down.html', {'resultat':tab_list, 'tab_dossier':info_dossier})

@login_required(login_url="/auth/auth_in/")
def downOnce(request, id):
	obj = SuiviUpload.objects.get(id__exact=id)
	filename = obj.fichiers.path
	file_path = os.path.join(settings.MEDIA_ROOT, filename)
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response

@login_required(login_url="/auth/auth_in/")
def downAll(request, id):
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

		img = open(file_path, "rb")
		img_read = img.read()

		zip.writestr(nom, img_read)

	zip.close()

	response = HttpResponse(content_type='application/zip')
	response["Content-Disposition"] = "attachement;filename=corelab.zip"

	in_memory.seek(0)
	response.write(in_memory.read())

	return response

# Gère la partie Admin Etudes
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
@login_required(login_url="/auth/auth_in/")
def adminetude(request):
	if request.method == 'POST':
		nom = request.POST['nom']

		user_current = request.user

		date_now = datetime.today()
		RefEtudes.objects.create(nom=nom, date_ouverture=date_now)
	
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
		type = request.POST['type']


		check_mdp = checkmdp(pass_first, pass_second)

		if check_mdp :
			nw_user = User.objects.create_user(
			username=username, password=pass_first, email=email)
			nw_user.save()

			if int(type) == 0:
				nw_user.is_staff = True
				nw_user.save()
			else:
				if nw_user.is_staff:
					nw_user.is_staff = False
					nw_user.save()
			
			if len(nom) > 0 and len(numero) > 0:
				date_now = datetime.today()
				nw_centre = RefInfocentre(nom=nom, numero=numero, date_ajout=date_now)
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
		type = request.POST['type']
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

		if int(type) == 0:
			user_info.is_staff = True
		else:
			if user_info.is_staff:
				user_info.is_staff = False
		user_info.save()

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
	
		date_now = datetime.today()
		nw_centre = RefInfocentre.objects.create(nom=nom, numero=numero, date_ajout=date_now)

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
			date_now = datetime.today()
			save_etude = RefEtudes.objects.get(pk=etude)
			nw_jonction = JonctionUtilisateurEtude.objects.create(user=user_info, etude=save_etude, date_autorisation=date_now)

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

@login_required(login_url="/auth/auth_in/")
def authDel(request):
	liste_etude = []
	liste_centre = []

	message = ""

	id_user = request.POST.get('val_user')
	id_search = request.POST.get('val_id')
	type_tab = request.POST.get('type_tab')

	user_info = User.objects.get(pk=id_user)

	if request.method == 'POST':
		form = FormsAutorisation()
		if type_tab == 'etude':
			user_etude = JonctionUtilisateurEtude.objects.get(id__exact=id_search)
			verif_suivi = SuiviUpload.objects.filter(etude__exact=user_etude)

			if not verif_suivi.exists():
				user_etude = JonctionUtilisateurEtude.objects.get(id__exact=id_search).delete()
				message = "Suppression des autorisations ont été appliquées"
			else:
				message = "Suppression annulée, cet utilisateur à chargé des documents :" + str(len(verif_suivi)) + " document(s) trouvés"

		elif type_tab == "centre":
			verif = SuiviUpload.objects.filter(id__exact=id_user)

			if not verif.exists():
				save_centre.user.remove(id_user)
				message = "Le centre n'est plus lié à cet utilisateur"
			else:
				message = "Cet utilisateur lié à ce centre a chargé des documents (" + str(len(verif)) + " document(s))"


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

def j_serial(o):     # self contained
    from datetime import datetime, date
    return str(o).split('.')[0] if isinstance(o, (datetime, date)) else None
