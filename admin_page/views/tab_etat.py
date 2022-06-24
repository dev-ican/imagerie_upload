# -*- coding: utf-8 -*-

import os

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from upload.models import RefEtapeEtude, RefEtatEtape, SuiviUpload
from ..filters import RefEtatEtapeFilter, RefEtapeEtudeFilter

from .module_log import information_log
from .module_views import (
    info_upload,
    centres_etude_selectionnee,
    gestion_etape,
    gestion_etude_recente,
    infos_etats_etape,
    nom_etape,
)

# Permet d'afficher la page des étapes de chaque étude
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------


@login_required(login_url="/auth/auth_in/")
def admin_up(request):
    """Affiche la page du tableau gérant les différents états des étapes d'une étude."""

    resultat = []
    list_centre = []
    donnees_de_l_upload = {}
    nbr_noms_etape = {}
    # etat_etape_filter = RefEtatEtapeFilter(request.GET, queryset=RefEtatEtape.objects.all())
    # etape_etude_filter = RefEtapeEtudeFilter(request.GET, queryset=RefEtapeEtude.objects.all())
    
    try:
        # etude_selectionne correspond à la dernière étude créée.
        etude_selectionnee = SuiviUpload.objects.get(id=SuiviUpload.objects.all().order_by("dossier", "date_upload")[:1])
    except ObjectDoesNotExist:
        return render(request, "admin_page_upload.html")

    try:
        # dossiers correspond aux objets "SuiviUpload" liés à l'étude selectionnée.
        dossiers = SuiviUpload.objects.filter(etude__etude__id=etude_selectionnee.etude.etude.id).distinct("dossier")

        # nbr_etape correspond au nombre d'étapes de l'étude selectionnée.
        nbr_etape = RefEtapeEtude.objects.filter(etude=etude_selectionnee.etude.etude).count()

        # noms_etape est une liste comprenant le nom des étapes liés à l'étude selectionnée.
        noms_etape = nom_etape(etude_selectionnee.etude.id)

    
        for dossier in dossiers:
            """
            La fonction info_upload renvoi un dictionnaire comprenant les données suivante :
                infos_upload["id_"] = suivi_upload.id
                infos_upload["Etudes"] = var_qc.controle_qualite.nom
                infos_upload["Etudes_id"] = var_qc.id
                infos_upload["id_patient"] = nom_de_l_etude[0].id_patient
                infos_upload["nbr_upload"] =  nbr_de_fichiers
            
            """
            donnees_de_l_upload = info_upload(dossier)
            infoetape = infos_etats_etape(dossier)
            var_etape = gestion_etape(noms_etape,
                                      infoetape,  
                                      nbr_etape,
                                      dossier,
                                      etude_selectionnee
                                      )
            if len(var_etape) == 2:
                donnees_de_l_upload["etape_etude"] = var_etape[1]
            donnees_de_l_upload["error"] = var_etape[0]
            resultat.append(dict(donnees_de_l_upload))

        nbr_noms_etape["nbr_etape"] = nbr_etape
        nbr_noms_etape["nom_etape"] = noms_etape
        list_centre = centres_etude_selectionnee(dossiers)
        gestion_info = gestion_etude_recente(etude_selectionnee,
                                             # dossiers,
                                             list_centre
                                             )
        print(f"gestion_info : {gestion_info}")
    except ObjectDoesNotExist:
        dossiers = ""
        gestion_info = gestion_etude_recente(etude_selectionnee,
                                             # dossiers,
                                             list_centre
                                             )

    nbr_entree = len(resultat)
    # Enregistrement du log-----------------------------
    nom_documentaire = "Affiche le tableau des études en cours"
    information_log(request, nom_documentaire)
    # --------------------------------------------------
    # print(resultat)
    # print(f"nbr_noms_etape : {nbr_noms_etape}")
    # V1_ADMIN_DATA_TAB.html > Nom de la template HTML pour la version V1
    return render(request, "admin_page_upload.html",{"resultat": resultat,
                                                    "nbr_noms_etape": nbr_noms_etape,
                                                    "str_etude": gestion_info[1],
                                                    "str_centre": gestion_info[0],
                                                    "nbr_entree": nbr_entree,
                                                    # "title_page":"Administration des étapes",
                                                    # "filter_etat_etape" : etat_etape_filter,
                                                    # "filter_etape_etude": etape_etude_filter
                                                    })


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
