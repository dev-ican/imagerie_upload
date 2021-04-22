# -*- coding: utf-8 -*-

import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from admin_page.forms import FormsAutorisation
from upload.models import JonctionUtilisateurEtude, RefInfocentre, SuiviUpload

from .module_log import (
    creation_log,
    edition_log,
    information_log,
    suppr_log,
)

# Gère la partie validation des comptes
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

@login_required(login_url="/auth/auth_in/")
def auth_compte(request):
    inactive_user = User.objects.filter(is_active=False)
    print(inactive_user)

    return render(
        request,
        "check_compte.html",
        {"resultat": inactive_user},
    )

@login_required(login_url="/auth/auth_in/")
def compte_valide(request):
    inactive_user = User.objects.filter(is_active=False)
    print(inactive_user)