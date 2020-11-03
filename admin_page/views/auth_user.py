# -*- coding: utf-8 -*-

import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from admin_page.forms import FormsAutorisation
from upload.models import JonctionUtilisateurEtude, RefInfocentre

from .module_admin import choice_centre, choice_etude
from .module_log import edition_log
from .module_views import del_auth, j_serial, jonc_centre

# Gère la partie autorisation
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------


@login_required(login_url="/auth/auth_in/")
def admin_auth(request):
    """Charge la page index pour l'autorisation des utilisateurs."""
    user_tab = User.objects.all().order_by("username")
    return render(
        request,
        "admin_autorisation.html",
        {"resultat": user_tab},
    )


@login_required(login_url="/auth/auth_in/")
def auth_edit(request, id_etape):
    """Charge la page d'édition des autorisations utilisateur."""
    liste_etude = []
    liste_centre = []
    user_info = User.objects.get(pk=id_etape)
    if request.method == "POST":
        form = FormsAutorisation()
        etude = request.POST["etude"]
        centre = request.POST["centre"]
        user_centre = RefInfocentre.objects.filter(
            user__id=id_etape
        ).filter(id=centre)
        user_etude = JonctionUtilisateurEtude.objects.filter(
            user=id_etape
        ).filter(etude__id=etude)
        # Enregistrement du log---------------------------------------
        # ------------------------------------------------------------
        nom_documentaire = (
            " a editer les autorisation de l'utilisateur : "
            + user_info.username
        )
        edition_log(request, nom_documentaire)
        # -------------------------------------------------------------
        # -------------------------------------------------------------
        jonc_centre(
            user_etude, etude, user_info, user_centre, centre
        )
    liste_etude = choiceEtude(True)
    liste_centre = choiceCentre(True)
    form = FormsAutorisation()
    form.fields["etude"].choices = liste_etude
    form.fields["etude"].initial = [0]
    form.fields["centre"].choices = liste_centre
    form.fields["centre"].initial = [0]
    user_centre = RefInfocentre.objects.filter(user__id=id_etape)
    user_etude = JonctionUtilisateurEtude.objects.filter(
        user=id_etape
    )
    return render(
        request,
        "admin_auth_edit.html",
        {
            "form": form,
            "etude": user_etude,
            "centre": user_centre,
            "user": user_info,
        },
    )


@login_required(login_url="/auth/auth_in/")
def auth_del(request):
    """Appel Ajax permettant la supression d'une autorisation."""
    id_user = request.POST.get("val_user")
    id_search = request.POST.get("val_id")
    type_tab = request.POST.get("type_tab")
    user_info = User.objects.get(pk=id_user)
    if request.method == "POST":
        message = del_auth(type_tab, id_search, request)
    user_centre = RefInfocentre.objects.filter(
        user__id=user_info.id
    )
    user_etude = JonctionUtilisateurEtude.objects.filter(
        user=user_info.id
    )
    var_etude = {}
    var_centre = {}
    x = 0
    for item in user_etude:
        date_j = j_serial(item.etude.date_ouverture)
        var_etude[x] = {
            "nom": item.etude.nom,
            "date": date_j,
            "type": "etude",
            "id_jonc": item.id,
            "id_user": user_info.id,
        }
        x += 1
    x = 0
    for item in user_centre:
        date_j = j_serial(item.date_ajout)
        var_centre[x] = {
            "nom": item.nom,
            "num": item.numero,
            "date": date_j,
            "type": "centre",
            "id_jonc": item.id,
            "id_user": user_info.id,
        }
        x += 1
    context = {
        "etude": var_etude,
        "centre": var_centre,
        "message": message,
    }
    creation_json = json.dumps(context)
    return HttpResponse(
        json.dumps(creation_json),
        content_type="application/json",
    )
