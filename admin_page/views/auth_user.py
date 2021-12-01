# -*- coding: utf-8 -*-

import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from admin_page.forms import FormsAutorisation, FormPwdChange
from upload.models import JonctionUtilisateurEtude, RefInfocentre, ValideCompte
from django.contrib import messages

from .module_admin import choice_centre, choice_etude, check_mdp
from .module_log import edition_log
from .module_views import del_auth, j_serial, jonc_centre, pwd_nw

# Gère la partie autorisation
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------


@login_required(login_url="/auth/auth_in/")
def admin_auth(request):
    """Charge la page index pour l'autorisation des utilisateurs."""
    user_tab = User.objects.all().order_by("username").select_related('Compte_Valider')
    return render(
        request,
        "admin_autorisation.html",
        {"resultat": user_tab},
    )


@login_required(login_url="/auth/auth_in/")
def auth_edit(request, id_etape):
    """Charge la page d'édition des autorisations utilisateur."""
    message = ""
    user_lock =  ValideCompte.objects.get(create_user__id=id_etape)
    grp_user = request.user.groups.filter(name="Administrateur service").exists()
    if user_lock.etat is None or user_lock.etat.id == 3 or grp_user :
        liste_etude = []
        liste_centre = []
        user_block = RefInfocentre.objects.filter(user__id=id_etape)
        user_info = User.objects.get(pk=id_etape)
        if request.method == "POST":
            if len(user_block) < 1:
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
            else:
                message = "Un utilisateur ne peut avoir qu'un centre"
    else:
        message = messages.add_message(
            request, messages.WARNING, "Ce compte est validé débloquer le pour pouvoir le modifier"
        )
        return redirect('/admin_page/userAuth/')
    liste_etude = choice_etude(True)
    liste_centre = choice_centre(True)
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
            "user_info": user_info,
            "messages":message,
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
        message = del_auth(type_tab, id_search, request,id_user)
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

@login_required(login_url="/auth/auth_in/")
def compte_user(request):
    user_current = request.user
    if request.method == "POST":
        mail = request.POST["email"]
        mdp_o = request.POST["nw_mdp"]
        mdp_t = request.POST["nw_mdp_second"]
        verif_pwd = check_mdp(mdp_o,mdp_t)
        pwd_nw(verif_pwd, mdp_o, mail, user_current)

    info = {
            "email": user_current.email,
        }
    form = FormPwdChange(info)
    return render(
        request,
        "V1_COMPTE.html",
        {
            "form": form,
        },
    )
