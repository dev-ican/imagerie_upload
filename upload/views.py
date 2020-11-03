# -*- coding: utf-8 -*-

import os
import zipfile

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import UploadForm
from .models import (
    DossierUpload, JonctionEtapeSuivi, JonctionUtilisateurEtude,
    RefControleQualite, RefEtapeEtude, RefEtatEtape, RefTypeAction,
    SuiviDocument, SuiviUpload, log)


@login_required(login_url="/auth/auth_in/")
def index(request):
    ''' Chargement de l'index, permet de charger
    les documents devant être listé sur la page d'accueille '''
    tab_etude = [] 
    date_now = timezone.now()
    user_current = request.user
    list_etude = JonctionUtilisateurEtude.objects.filter(user=user_current)
    for item in list_etude:
        tab_etude.append(item.etude.id)
    doc_list = SuiviDocument.objects.filter(etude__id__in=tab_etude)
    type_action = RefTypeAction.objects.get(pk=4)
    log.objects.create(
        user=user_current,
        action=type_action,
        date=date_now,
        info="Visite de l'index",
    )

    return render(
        request,
        "index.html",
        {"response": doc_list, "user": user_current},
    )


@login_required(login_url="/auth/auth_in/")
def contact(request):
    '''Charge la page d'acceuille et
    renvois les contacts déjà entrés '''
    date_now = timezone.now()
    user_current = request.user
    type_action = RefTypeAction.objects.get(pk=4)
    log.objects.create(
        user=user_current,
        action=type_action,
        date=date_now,
        info="Visite des contacts",
    )
    return render(request, "contact.html")


@login_required(login_url="/auth/auth_in/")
def formulaire(request):
    ''' Charge la page du formulaire de chargement.'''
    date_now = timezone.now()
    user_current = request.user
    liste_protocole = []
    # Si le formulaire est envoyé
    if request.method == "POST":
        # Renseignement de la table de Log
        type_action = RefTypeAction.objects.get(pk=4)
        log.objects.create(
            user=user_current,
            action=type_action,
            date=date_now,
            info="Utilisation du formulaire pour envois de donnée",
        )
        # Récupération des données du formulaire
        etude = request.POST["etudes"]
        nip = request.POST["nip"]
        date = request.POST["date_irm"]
        id_etude = JonctionUtilisateurEtude.objects.get(
            id__exact=etude
        )
        id_qc = RefControleQualite.objects.get(id=1)
        id_etape = RefEtatEtape.objects.get(id=1)
        id_etapes = RefEtapeEtude.objects.filter(
            etude=id_etude.etude.id
        )
        date_now = timezone.now()
        filez = request.FILES.getlist("upload")
        # Création du dossier en lien avec les fichiers chargés
        create_jonction = DossierUpload(
            user=user_current, controle_qualite=id_qc, date=date
        )
        create_jonction.save()
        # Création dans la table suivi upload de
        #chaque fichier chargé en lien avec le dossier
        for f in filez:
            create_suivi = SuiviUpload(
                user=user_current,
                etude=id_etude,
                id_patient=nip,
                date_upload=date_now,
                date_examen=date,
                fichiers=f,
                dossier=create_jonction,
            )
            name_file = f.name
            create_suivi.save()
            # Si le fichier chargé est une archive alors décompréssé
            # Supprime l'archive à la fin
            if name_file.find(".zip") != -1:
                zipfile_save = zipfile.ZipFile(
                    create_suivi.fichiers.path, mode="r"
                )
                path = os.path.dirname(create_suivi.fichiers.path)
                zipfile_save.extractall(path)
                zipfile_save.close()
                if os.path.exists(create_suivi.fichiers.path):
                    os.remove(create_suivi.fichiers.path)
        # Création de chaque étapes pour le patient chargé
        for etape in id_etapes:
            create_etape = JonctionEtapeSuivi.objects.create(
                upload=create_jonction, etape=etape, etat=id_etape
            )
        var_url = "/upload/form/"
        return redirect(var_url)
    form = UploadForm()
    # Charge les listes déroulantes
    request_utilisateur_protocole = (
        JonctionUtilisateurEtude.objects.filter(
            user=user_current.id
        )
    )
    for util_pro in request_utilisateur_protocole:
        collapse = (util_pro.id, util_pro.etude.nom)
        liste_protocole.append(collapse)
    liste_protocole.append((0, "Séléctionner une étude"))
    form.fields["etudes"].choices = liste_protocole
    form.fields["etudes"].initial = [0]
    return render(request, "form_upload.html", {"form": form})
