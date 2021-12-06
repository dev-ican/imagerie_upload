# -*- coding: utf-8 -*-


import json
from os.path import isdir

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from datetime import datetime

from upload.models import (DossierUpload, JonctionEtapeSuivi, RefEtapeEtude,
                           RefEtatEtape, RefEtudes, SuiviUpload)

from .module_log import information_log

# Gère la page statistique
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------


@login_required(login_url="/auth/auth_in/")
def admin_page(request):
    """Permet d'afficher la page de statistique."""
    user_current = request.user
    dict_etat = {}
    list_etude = RefEtudes.objects.all()
    list_etat = RefEtatEtape.objects.all()
    for etude in list_etude:
        exist_etude = SuiviUpload.objects.filter(
            etude__etude=etude.id
        ).distinct("dossier")
        resume_etat = {}
        resume_etat["data"] = json.dumps(
            {"nbr": [exist_etude.count()], "nom": [etude.nom]}
        )
        if exist_etude.exists():
            # Réalise certain calcul à ramener dans le graph
            for etat in list_etat:
                nbr_qc_ok = 0
                nbr_qc_not = 0
                nbr_qc_nw = 0
                for dossier in exist_etude:
                    try:
                        qc_dossier = DossierUpload.objects.get(
                            id=dossier.dossier.id
                        )
                        if qc_dossier.controle_qualite.id == 1:
                            nbr_qc_nw += 1
                        elif qc_dossier.controle_qualite.id == 2:
                            nbr_qc_ok += 1
                        elif qc_dossier.controle_qualite.id == 3:
                            nbr_qc_not += 1
                    except ObjectDoesNotExist:
                        # Enregistrement du log-------------------
                        # ----------------------------------------
                        nom_documentaire = " a provoqué une erreur le dossier patient n'existe pas"
                        information_log(request, nom_documentaire)
                        # ----------------------------------------
                        # ----------------------------------------
                    nbr_etat = (
                        JonctionEtapeSuivi.objects.filter(
                            upload__exact=dossier.dossier
                        )
                        .filter(etat__exact=etat)
                        .count()
                    )
                    resume_etat[etat.nom] = nbr_etat
            resume_etat["Nouveau"] = nbr_qc_nw
            resume_etat["Refused"] = nbr_qc_not
            resume_etat["Passed"] = nbr_qc_ok
            dict_etat[etude.nom] = resume_etat
    # Enregistrement du log-----------------------------------
    # --------------------------------------------------------
    nom_documentaire = " Affiche la page graphique"
    information_log(request, nom_documentaire)
    # --------------------------------------------------------
    # --------------------------------------------------------
    tab_list = {}
    list_tab = []
    # Savoir si des étape se nomme : téléchargement, download
    list_nom = ["téléchargement","download","Téléchargement","Download", "Upload"]
    list_filter = RefEtapeEtude.objects.filter(nom__in=list_nom)
    for item in list_filter:
        id_etape = item.id
        jonc_dossier = JonctionEtapeSuivi.objects.filter(etape=id_etape).filter(etat=1)
        for object in jonc_dossier:
            dict_object = {}
            dossier_result = SuiviUpload.objects.filter(dossier=object.upload.id)
            dossier_first = dossier_result[0]
            date_ex =datetime.strftime(dossier_first.date_examen,'%Y-%m-%d')
            date_up = datetime.strftime(dossier_first.date_upload,'%Y-%m-%d')
            dict_object[dossier_first.id_patient] = {
            "id": dossier_first.id,
            "nip": dossier_first.id_patient,
            "date_exam": date_ex,
            "date_upload": date_up,
            "user": dossier_first.user.username,
            }
            list_tab.append([dossier_first.id_patient,date_ex,date_up,dossier_first.user.username,])
    creation_json = json.dumps(tab_list)

    return render(
        request, "admin_page.html", {"nbr_etat": dict_etat, "list_json":list_tab, 'title_page':'Accueil Administration de l\'application Upload'}
    ) #V1_ADMIN_STAT.html
