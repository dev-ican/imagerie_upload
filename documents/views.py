from django.shortcuts import render
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

from .forms import DocumentForm
from upload.models import RefEtudes, JonctionUtilisateurEtude, RefEtapeEtude, RefInfocentre, JonctionEtapeSuivi, RefEtatEtape, SuiviDocument, SuiviDocument

from datetime import date, time, datetime
# Create your views here.
@login_required(login_url="/auth/auth_in/")
def gestiondoc(request):

	if request.method == 'POST':
		titre = request.POST['titre']
		desc = request.POST['description']
		etude = request.POST['etudes']
		type = request.POST['type']

		if type == str(0):
			url_img = 'bg-nw-info.jpg'
		elif type == str(1):
			url_img = 'bg-nw-protocole.jpg'

		print(settings.BASE_DIR)

		path_img = settings.BASE_DIR + url_img
		id_etude = RefEtudes.objects.get(id__exact=etude)
		
		date_now = datetime.today()
		user_current = request.user
		filez = request.FILES.getlist('document')

		for f in filez:
			create_suivi = SuiviDocument(user=user_current, etude=id_etude, titre=titre, description=desc, date=date_now, fichiers=f, background=url_img)
			create_suivi.save()
	
	form = DocumentForm()

	request_etude = RefEtudes.objects.all()

	liste_protocole = choiceEtude(True)

	form.fields['etudes'].choices = liste_protocole
	form.fields['etudes'].initial = [0]

	doc_tab = SuiviDocument.objects.all()
	return render(request,
		'admin_docu.html',{"form":form, 'resultat':doc_tab})

@login_required(login_url="/auth/auth_in/")
def downOnce(request, id):
	obj = SuiviDocument.objects.get(id__exact=id)
	filename = obj.fichiers.path
	file_path = os.path.join(settings.MEDIA_ROOT, filename)
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response

def choiceEtude(val_zero):
	liste_etude = []
	request_etude = RefEtudes.objects.all()

	for util_pro in enumerate(request_etude):
		collapse = (util_pro[1].id,util_pro[1].nom)
		liste_etude.append(collapse)

	if val_zero == True:
		liste_etude.append((0,"Séléctionner une étude"))

	return liste_etude