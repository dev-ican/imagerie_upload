from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import UploadForm
from .models import RefEtudes, JonctionUtilisateurEtude

# Create your views here.

@login_required(login_url="/auth/auth_in/")
def index(request):

	    return render(request,
                  'index.html')

@login_required(login_url="/auth/auth_in/")
def contact(request):

	    return render(request,
                  'contact.html')

@login_required(login_url="/auth/auth_in/")
def formulaire(request):
	user_current = request.user
	liste_protocole = [("0", "Vos études")]
	x = 0

	if request.method == 'POST':
		form = UploadForm(request.POST)

	else:
		form = UploadForm()
		request_utilisateur_protocole = JonctionUtilisateurEtude.objects.filter(user__exact=user_current.id)

		for util_pro in request_utilisateur_protocole:
			x += 1
			collapse = (str(x),str(util_pro.etude))
			liste_protocole.append(collapse)

		form.fields['etudes'].choices = liste_protocole
		form.fields['etudes'].initial = [0]

	return render(request, 'form_upload.html', {'form': form})

