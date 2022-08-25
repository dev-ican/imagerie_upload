# -*- coding: utf-8 -*-

# from ensurepip import bootstrap
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.urls import reverse_lazy

from upload.models import RefEtapeEtude, SuiviUpload, RefInfoCentre, RefEtudes
from ..forms import FormSelectionEtudeEtape, FormSelectionEtudeURC

from .module_log import information_log
from .module_views import (
    info_upload,
    centres_etude_selectionnee,
    gestion_etape,
    # gestion_etude_selectionnee,
    infos_etats_etape,
    nom_etape,
)

# Permet d'afficher la page des étapes de chaque étude
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

@login_required(login_url="/auth/auth_in/")
def admin_up(request, etude_id="4", centre_id="1"):
    """Affiche la page du tableau gérant les différents états des étapes d'une étude."""

    resultat = []
    donnees_de_l_upload = {}
    nbr_noms_etape = {}


    if request.method == "POST":

        urc_users = User.objects.filter(groups__name="URC")

        if request.user in urc_users:
            form = FormSelectionEtudeURC(request.POST)
        else:
            form = FormSelectionEtudeEtape(request.POST)

        if form.is_valid():
            centre_choisi_id = form.cleaned_data["centre_choice"]
            etude_choisie_id = form.cleaned_data["etude_choice"]

            try:
                # etude_selectionnee correspond à la dernière étude créée.
                etude_selectionnee = RefEtudes.objects.get(id=etude_choisie_id)
                centre_selectionnee = RefInfoCentre.objects.get(id=centre_choisi_id)

            except ObjectDoesNotExist:
                return render(request, "admin_page_upload.html")

            try:
                # "dossiers_lies_a_l_etude" correspond aux objets "SuiviUpload" liés à l'étude selectionnée.
                dossiers_lies_a_l_etude = SuiviUpload.objects.filter(etude__etude__id=etude_choisie_id)
                dossiers_lies_a_l_etude = dossiers_lies_a_l_etude.filter(user__in=centre_selectionnee.user.all())
                
                nbr_etape = RefEtapeEtude.objects.filter(etude=etude_selectionnee).count()

                # noms_etape est une liste comprenant le nom des étapes liés à l'étude selectionnée.
                noms_etape = nom_etape(etude_selectionnee)
            
                for dossier in dossiers_lies_a_l_etude:
                    """
                    La fonction info_upload renvoi un dictionnaire comprenant les données suivante :
                    infos_upload = {}
                    infos_upload["suivi_upload_id"] = suivi_upload.id
                    infos_upload["qc_nom"] = var_qc.controle_qualite.nom
                    infos_upload["qc_id"] = var_qc.id
                    infos_upload["id_patient"] = upload[0].id_patient
                    infos_upload["date_examen"] = upload[0].date_examen            
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

                centres_etude_selec = centres_etude_selectionnee(dossiers_lies_a_l_etude)
                # print(f"centre_etude_selectionne : {centres_etude_selec}")

                nbr_entree = len(resultat)

            except ObjectDoesNotExist:
                dossiers = ""

    else:
        form = FormSelectionEtudeEtape()
        resultat = None
        nbr_entree = None


    # Enregistrement du log-----------------------------
    nom_documentaire = "Affiche le tableau des études en cours"
    information_log(request, nom_documentaire)
    # --------------------------------------------------
    # V1_ADMIN_DATA_TAB.html > Nom de la template HTML pour la version V1

    # print(resultat)
  
    return render(request, "admin_page_upload.html",{"resultat": resultat,
                                                    "nbr_noms_etape": nbr_noms_etape,
                                                    "nbr_entree": nbr_entree,
                                                    "form": form,
                                                    })


@login_required(login_url="/auth/auth_in/")
def aff_dossier(request, id_suivi):
    """Lors du clic sur un dossier chargé dans le tableau des étapes, cela
    appel le module qui affiche les fichiers chargés pour le patient donné."""
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