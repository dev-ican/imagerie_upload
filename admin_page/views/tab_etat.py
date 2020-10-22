from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
from .module_views import *
from .module_log import *
from django.core.exceptions import ObjectDoesNotExist

from upload.models import (
    RefEtapeEtude,
    SuiviUpload
)

# Permet d'afficher la page des étapes de chaque étude
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------


@login_required(login_url="/auth/auth_in/")
def adminup(request):
    """ Affiche la page du tableau gérant
    les différents état des étapes d'une étude. """
    tab_list = []
    list_centre = []
    dict_upload = {}
    dict_nbr = {}
    etude_recente = SuiviUpload.objects.get(
        id=SuiviUpload.objects.all().order_by(
            "dossier", "date_upload"
        )[:1]
    )
    try:
        dossier_all = SuiviUpload.objects.filter(
            etude=etude_recente.etude
        ).distinct("dossier")
        nbr_etape = RefEtapeEtude.objects.filter(
            etude=etude_recente.etude.etude
        ).count()
        nom_etape = nomEtape(etude_recente)
        for files in dossier_all:
            dict_upload = {}
            dict_upload = dictUpload(dict_upload, files)
            info_etape = infoEtape(files)
            var_etape = gestionetape(nom_etape, info_etape, nbr_etape)
            if len(var_etape) == 2:
                dict_upload["etape_etude"] = var_etape[1]
            dict_upload["error"] = var_etape[0]
            tab_list.append(dict_upload)
        dict_nbr["nbr_etape"] = nbr_etape
        dict_nbr["nom_etape"] = nom_etape
        list_centre = etudeRecente(etude_recente, dossier_all)
        gestion_info = gestionEtudeRecente(
            etude_recente, dossier_all, list_centre
        )
    except ObjectDoesNotExist:
        dossier_all = ""
        gestion_info = gestionEtudeRecente(
            etude_recente, dossier_all, list_centre
        )
    nbr_entrée = len(tab_list)
    # Enregistrement du log-----------------------------
    # --------------------------------------------------
    nom_documentaire = " Affiche le tableau des études en cours"
    informationLog(request, nom_documentaire)
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
        },
    )


@login_required(login_url="/auth/auth_in/")
def affdossier(request, id_suivi):
    """Lors du clic sur un dossier chargé dans le tableau des étapes,
    cela appel le module qui affiche les fichiers
    chargé pour le patient donné"""
    tab_list = []
    var_suivi = SuiviUpload.objects.get(id=id_suivi)
    path = os.path.dirname(var_suivi.fichiers.path)
    list_dir = os.listdir(path)
    for item in list_dir:
        lien_id = os.path.join(path, item)
        dict_list = {}
        if os.path.isdir(lien_id):
            for root, dirs, files in os.walk(lien_id, topdown=False):
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
            dict_list = {"nom": item, "url": lien_id, "dir": False}
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
    informationLog(request, nom_documentaire)
    # -------------------------------------------------------
    # -------------------------------------------------------
    return render(
        request,
        "admin_page_down.html",
        {"resultat": tab_list, "tab_dossier": info_dossier},
    )
