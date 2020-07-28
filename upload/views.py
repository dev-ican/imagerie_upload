from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import LogIn, FormUpload

# Create your views here.

@login_required(login_url="/upload/auth_in/")
def index(request):

	    return render(request,
                  'index.html')


def formulaire(request):

	if request.method == 'POST':
		form = FormUpload(request.POST)

	else:
		form = FormUpload()
		form.fields['protocoles'].choices = [('1',"Protocoles de l'utilisateur")]
		form.fields['protocoles'].initial = [1]

	return render(request, 'form_upload.html', {'form': form})

def get_login(request):
    ''' Permet de se connecter au: site
    Allows you to connect to the site '''

    if request.method == 'POST':
        form = LogIn(request.POST)
        username = request.POST['log_id']
        password = request.POST['pwd']
        user = authenticate(request, username=username, password=password)
        if form.is_valid():
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/upload/")
    else:
        form = LogIn()

    return render(
        request, 'auth.html', {'form': form})

def log_out(request):
    ''' Permet de se déconnecter
    Allows to disconnect '''
    logout(request)
    messages.add_message(
        request,
        messages.WARNING,
        "Vous êtes maintenant déconnecté")
    return redirect('/upload/')