from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import LogIn


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
