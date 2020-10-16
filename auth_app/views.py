from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import LogIn
from upload.models import log, RefTypeAction
from django.utils import timezone


def get_login(request):
    ''' Permet de se connecter au site
    Allows you to connect to the site '''

    if request.method == 'POST':
        form = LogIn(request.POST)
        username = request.POST['log_id']
        password = request.POST['pwd']
        user = authenticate(request, username=username, password=password)
        if form.is_valid():
            if user is not None:
                login(request, user)
                #Enregistrement du log------------------------------------------------------------------------
                #---------------------------------------------------------------------------------------------
                date_now = timezone.now()
                user_current = request.user
                type_action = RefTypeAction.objects.get(pk=5)
                nom_documentaire = "Connexion de l'utilisateur " + str(user_current.username)
                log.objects.create(user=user_current, action=type_action, date=date_now, info=nom_documentaire)
                #----------------------------------------------------------------------------------------------
                #----------------------------------------------------------------------------------------------
                return HttpResponseRedirect("/upload/")
    else:
        form = LogIn()

    return render(
        request, 'auth.html', {'form': form})

def log_out(request):
    ''' Permet de se déconnecter
    Allows to disconnect '''
    #Enregistrement du log------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------
    date_now = timezone.now()
    user_current = request.user
    type_action = RefTypeAction.objects.get(pk=6)
    nom_documentaire = "Deconnexion de l'utilisateur " + str(user_current.username)
    log.objects.create(user=user_current, action=type_action, date=date_now, info=nom_documentaire)
    #----------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------
    logout(request)
    messages.add_message(
        request,
        messages.WARNING,
        "Vous êtes maintenant déconnecté")
    return redirect('/upload/')
