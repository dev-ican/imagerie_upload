# -*- coding: utf-8 -*-

import json

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from admin_page.forms import FormsAutorisation
from upload.models import ValideCompte, RefEtatValideCompte
from datetime import datetime
from django.utils import timezone
from .module_views import send_mail
from django.contrib import messages

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

from django.contrib.auth.models import Group
group_name = "Collaborateurs"

# group_permissions = Group.objects.get(name=group_name).permissions.all()
# print(group_permissions)

# for group in Group.objects.all():
#     permissions = group.permissions.filter(name__contains = "Collaborateurs")
#     print(permissions)


@login_required(login_url="/auth/auth_in/")
def auth_compte(request):
    message = ""
    inactive_user = User.objects.filter(is_active=False).select_related('Compte_Valider')
    valide_user = User.objects.filter(is_active=True).select_related('Compte_Valider')

    return render(
        request,
        "check_compte.html",
        {"resultat": inactive_user,
        "dict_check" : valide_user},
    )

@login_required(login_url="/auth/auth_in/")
@staff_member_required
def compte_valide(request, id_user):
    # Mise à jour de la table validation
    check_user = ValideCompte.objects.get(create_user=id_user)
    check_user.date_validation = timezone.now()
    check_user.validateur = request.user
    check_user.etat = RefEtatValideCompte.objects.get(pk=2)

    # Activation du compte
    activate_user = User.objects.get(pk=id_user)
    activate_user.is_active = True

    # Propriété et appel de la fonction d'envois de mail
    origin = 'valider'
    check = [check_user.demandeur.email]
    send_mail(request.user,User.objects.get(pk=id_user),check,origin)

    # Message à afficher aux utilisateurs
    message = messages.add_message(
        request, messages.WARNING, "Ouverture du compte effectuée"
    )

    # Sauvegarde des modifications dans la BDD
    activate_user.save()
    check_user.save()
    return redirect('/admin_page/authacc/', {"message" : message })

@login_required(login_url="/auth/auth_in/")
@staff_member_required
def compte_refus(request, id_user):
    # Mise à jour de la table validation
    check_user = ValideCompte.objects.get(create_user=id_user)
    check_user.date_validation = timezone.now()
    check_user.validateur = request.user
    check_user.etat = RefEtatValideCompte.objects.get(pk=3)

    # Propriété et appel de la fonction d'envois de mail
    origin = 'refus'
    check = [check_user.demandeur.email]
    send_mail(request.user,User.objects.get(pk=id_user),check,origin)

    # Message à afficher aux utilisateurs
    message = messages.add_message(
        request, messages.WARNING, "Le refus a été notifié au demandeur"
    )

    # Sauvegarde des modifications dans la BDD
    check_user.save()
    return redirect('/admin_page/authacc/', {"message" : message })

@login_required(login_url="/auth/auth_in/")
def compte_verif(request, id_user):

    check_user = ValideCompte.objects.get(create_user=id_user)
    check_user.date_demande = timezone.now()
    check_user.demandeur = request.user
    check_user.etat = RefEtatValideCompte.objects.get(pk=1)

    origin = 'verification'
    check = ['support_si@ican-institute.org']
    send_mail(request.user,User.objects.get(pk=id_user),check,origin)

    message = messages.add_message(
        request, messages.WARNING, "Envoi de votre demande effectué"
    )
    check_user.save()
    return redirect('/admin_page/authacc/', {"message" : message })

@login_required(login_url="/auth/auth_in/")
def compte_edit(request, id_user):

    check_user = ValideCompte.objects.get(create_user=id_user)
    check_user.date_edit = timezone.now()
    check_user.demandeur_edit = request.user
    check_user.etat = None

    # Désactivation du compte
    activate_user = User.objects.get(pk=id_user)
    activate_user.is_active = False

    #origin = 'editer'
    #check = ['support_si@ican-institute.org']
    #send_mail(request.user,User.objects.get(pk=id_user),check,origin)

    message = messages.add_message(
        request, messages.WARNING, "Le compte est désactivé et peut être édité"
    )

    activate_user.save()
    check_user.save()
    return redirect('/admin_page/authacc/', {"edition_check" : message })

