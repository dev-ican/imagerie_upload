# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from admin_page.forms import FormsUser, FormsUserEdit
from upload.models import JonctionUtilisateurEtude, SuiviUpload

from .module_admin import check_mdp
from .module_log import (
    creation_log,
    edition_log,
    information_log,
    suppr_log,
)
from .module_views import edit_password, creation_utilisateur

# Gère la partie Admin Utilisateur
# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------


@login_required(login_url="/auth/auth_in/")
def admin_user(request):
    """Charge la page index pour l'ajout ou l'édition d'un utilisateur."""

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        centre = request.POST["centre"]
        # numero = request.POST["numero"]
        pass_first = request.POST["pass_first"]
        pass_second = request.POST["pass_second"]
        type = request.POST["type"]

        checkmdp = check_mdp(pass_first, pass_second)
        creation_utilisateur(checkmdp,
                    type,
                    centre,
                    # numero,
                    username,
                    pass_first,
                    email,
                    )

        # Enregistrement du log-----------------------------------
        # --------------------------------------------------------
        nom_documentaire = " a créé l'utilisateur : " + username
        creation_log(request, nom_documentaire)
        # --------------------------------------------------------
        # --------------------------------------------------------

    form = FormsUser()
    user_tab = User.objects.all().order_by("username").select_related('Compte_Valider')

    return render(request, "admin_user.html", {"form": form,
                                               "resultat": user_tab
                                               })


@login_required(login_url="/auth/auth_in/")
def user_edit(request, id_etape):
    """Charge la page d'édition des utilisateurs."""
    if request.method == "POST":
        form = FormsUserEdit()
        type = request.POST["type"]
        username = request.POST["username"]
        email = request.POST["email"]
        pass_first = request.POST["pass_first"]
        pass_second = request.POST["pass_second"]
        user_info = User.objects.get(pk=id_etape)
        # Enregistrement du log-------------------
        # ----------------------------------------
        nom_documentaire = (
            " a editer l'utilisateur (id): "
            + str(user_info.username)
            + " ("
            + str(user_info.id)
            + ")"
        )
        edition_log(request, nom_documentaire)
        # ----------------------------------------
        # ----------------------------------------
        checkmdp = check_mdp(pass_first, pass_second)
        edit_password(
            checkmdp,
            type,
            username,
            pass_first,
            email,
            user_info,
        )
        return HttpResponseRedirect("/admin_page/viewUser/")
    else:
        user_info = User.objects.get(pk=id_etape)
        info = {
            "username": user_info.username,
            "email": user_info.email,
        }
        form = FormsUserEdit(info)
        # Enregistrement du log--------------------------
        # -----------------------------------------------
        nom_documentaire = (
            " a ouvert l'édition pour l'utilisateur : "
            + user_info.username
        )
        information_log(request, nom_documentaire)
        # -----------------------------------------------
        # -----------------------------------------------
    user_tab = User.objects.all().order_by("username")
    return render(
        request,
        "admin_user_edit.html",
        {
            "form": form,
            "resultat": user_tab,
            "select": int(id_etape),
        },
    )


@login_required(login_url="/auth/auth_in/")
def user_del(request, id_etape):
    """Appel Ajax permettant la supression d'un utilisateur."""
    x = 0
    if request.method == "POST":
        suppr = True
        info_suivi = User.objects.get(id=id_etape)
        info_upload = SuiviUpload.objects.filter(user__id=info_suivi.id)
        if info_upload.exists():
            for nbr in info_upload :
                x += 1
            suppr = False
        if suppr:
            # Enregistrement du log-----------------------------------
            # --------------------------------------------------------
            nom_documentaire = (
                " a supprimé l'utilisateur : "
                + info_suivi.username
            )
            suppr_log(request, nom_documentaire)
            # --------------------------------------------------------
            # --------------------------------------------------------
            exist_jonction = (
                JonctionUtilisateurEtude.objects.filter(
                    user__id__exact=info_suivi.id
                )
            )
            if exist_jonction.exists():
                JonctionUtilisateurEtude.objects.get(
                    user=info_suivi
                ).delete()
            User.objects.get(id=id_etape).delete()
            message = messages.add_message(
                request, messages.WARNING, "Suppression Faite"
            )
        else:
            if x == 0:
                terme = "suivi"
            else:
                terme = "suivis"
            message = messages.add_message(
                request,
                messages.WARNING,
                "Suppression annulée, cette étape est liée à : "
                + str(x)
                + terme,
            )
            # Enregistrement du log--------
            # -----------------------------
            nom_documentaire = (
                " à reçu un message d'erreur de suppression pour l'utilisateur : "
                + info_suivi.username
            )
            information_log(request, nom_documentaire)
            # -----------------------------
            # -----------------------------
    form = FormsUser()
    user_tab = User.objects.all().order_by("username")
    context = {
        "form": form,
        "resultat": user_tab,
        "message": message,
    }
    return render(request, "admin_user.html", context)
