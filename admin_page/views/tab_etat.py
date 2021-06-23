# -*- coding: utf-8 -*-

import os

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from upload.models import RefEtapeEtude, SuiviUpload

from .module_log import information_log
from .module_views import (
    dict_upload,
    etude_recente,
    gestion_etape,
    gestion_etude_recente,
    info_etape,
    nom_etape,
)

# Permet d'afficher la page des étapes de chaque étude
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------


@login_required(login_url="/auth/auth_in/")
def admin_up(request):
    """Affiche la page du tableau gérant les différents état des étapes d'une
    étude."""
    tab_list = []
    list_centre = []
    dictupload = {}
    dict_nbr = {}

    try:
        etuderecente = SuiviUpload.objects.get(
            id=SuiviUpload.objects.all().order_by(
                "dossier", "date_upload"
            )[:1]
        )
    except ObjectDoesNotExist:
        return render(request, "admin_page_upload.html")

    try:
        dossier_all = SuiviUpload.objects.filter(
            etude__etude__id=etuderecente.etude.etude.id
        ).distinct("dossier")
        nbr_etape = RefEtapeEtude.objects.filter(
            etude=etuderecente.etude.etude
        ).count()
        nometape = nom_etape(etuderecente.etude.id)
        print(dossier_all, etuderecente.etude)
        for files in dossier_all:
            dictupload = {}
            dictupload = dict_upload(dictupload, files)
            infoetape = info_etape(files)
            var_etape = gestion_etape(
                nometape, infoetape, nbr_etape
            )
            if len(var_etape) == 2:
                dictupload["etape_etude"] = var_etape[1]
            dictupload["error"] = var_etape[0]
            tab_list.append(dict(dictupload))
        dict_nbr["nbr_etape"] = nbr_etape
        dict_nbr["nom_etape"] = nometape
        list_centre = etude_recente(etuderecente, dossier_all)
        gestion_info = gestion_etude_recente(
            etuderecente, dossier_all, list_centre
        )
    except ObjectDoesNotExist:
        dossier_all = ""
        gestion_info = gestion_etude_recente(
            etuderecente, dossier_all, list_centre
        )
        '''return render(
                request,
                "admin_page_upload.html",
                {
                    "resultat": tab_list,
                    "dict_nbr": dict_nbr,
                    "str_etude": gestion_info[1],
                    "str_centre": gestion_info[0],
                    "taille": 0,
                    "debug": infoetape,
                },
        )'''

    nbr_entrée = len(tab_list)
    # Enregistrement du log-----------------------------
    # --------------------------------------------------
    nom_documentaire = " Affiche le tableau des études en cours"
    information_log(request, nom_documentaire)
    # --------------------------------------------------
    # --------------------------------------------------
    return render(
        request,
        "admin_page_upload.html",
        {
            "resultat": tab_list,
            "dict_nbr": dict_nbr,
            "str_etude": gestion_info[1],
            "str_centre": gestion_info[0],
            "taille": nbr_entrée,
            "debug" : dict_nbr,
        },
    )


@login_required(login_url="/auth/auth_in/")
def aff_dossier(request, id_suivi):
    """Lors du clic sur un dossier chargé dans le tableau des étapes, cela
    appel le module qui affiche les fichiers chargé pour le patient donné."""
    tab_list = []
    var_suivi = SuiviUpload.objects.get(id=id_suivi)
    path = os.path.dirname(var_suivi.fichiers.path)
    list_dir = os.listdir(path)
    for item in list_dir:
        lien_id = os.path.join(path, item)
        dict_list = {}
        if os.path.isdir(lien_id):
            for root, dirs, files in os.walk(
                lien_id, topdown=False
            ):
                x = 0
                y = 0
                for name in files:
                    x += 1
                for name in dirs:
                    y += 1
            dict_list = {
                "nom": item,
                "url": lien_id,
                "dir": True,
                "file": x,
                "direct": y,
            }
        else:
            dict_list = {
                "nom": item,
                "url": lien_id,
                "dir": False,
            }
        tab_list.append(dict_list)
    info_dossier = {
        "id": var_suivi.id_patient,
        "etude": var_suivi.etude.etude.nom,
        "id_etude": var_suivi.etude.etude.id,
        "lien": var_suivi.id,
        "path": path,
    }
    # Enregistrement du log----------------------------------
    # -------------------------------------------------------
    nom_documentaire = (
        " a listé les informations du patient : "
        + var_suivi.id_patient
    )
    information_log(request, nom_documentaire)
    # -------------------------------------------------------
    # -------------------------------------------------------
    return render(
        request,
        "admin_page_down.html",
        {"resultat": tab_list, "tab_dossier": info_dossier},
    )
