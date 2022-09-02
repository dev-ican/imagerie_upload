# -*- coding: utf-8 -*-


from genericpath import exists
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
    
    dict_etat = {}
    etudes = RefEtudes.objects.all()
    etats = RefEtatEtape.objects.all()

    for etude in etudes:
        suivis_upload = SuiviUpload.objects.filter(etude__etude=etude.id).distinct("dossier")
        resume_etat = {}
        resume_etat["data"] = json.dumps({"nbr_suivi": [suivis_upload.count()],
                                          "nom_etude": [etude.nom]
                                          })
        # resume_etat["data"] = json.dumps({"nbr": [suivis_upload.count()],
        #                                   "nom": [etude.nom]
        #                                   })


        # print(f"suivis_upload : {suivis_upload}")
        if suivis_upload.exists():
            # TODO ajouter les refus RGPD dans le graphique quand ils seront intégrés dans la page de suivi des études.

            # Réalise certain calcul à ramener dans le graph
            for etat in etats:
                nbr_qc_passed = 0
                nbr_qc_refused_technical = 0
                nbr_qc_new = 0
                for suivi_upload in suivis_upload:
                    try:
                        qc_dossier = DossierUpload.objects.get(id=suivi_upload.dossier.id)
                        if qc_dossier.controle_qualite.id == 1:
                            nbr_qc_new += 1
                        elif qc_dossier.controle_qualite.id == 2:
                            nbr_qc_passed += 1
                        elif qc_dossier.controle_qualite.id == 3:
                            nbr_qc_refused_technical += 1

                    except ObjectDoesNotExist:

                        # Enregistrement du log-------------------
                        # ----------------------------------------
                        nom_documentaire = " a provoqué une erreur le dossier patient n'existe pas"
                        information_log(request, nom_documentaire)
                        # ----------------------------------------
                        # ----------------------------------------

                    nbr_etat = (JonctionEtapeSuivi.objects.filter(upload__exact=suivi_upload.dossier).filter(etat__exact=etat).count())
                    resume_etat[etat.nom] = nbr_etat
            resume_etat["QC Nouveau"] = nbr_qc_new
            resume_etat["QC Refusé : Technique"] = nbr_qc_refused_technical
            resume_etat["QC Accepté"] = nbr_qc_passed
            # resume_etat["Nouveau"] = nbr_qc_new
            # resume_etat["Refused"] = nbr_qc_refused_technical
            # resume_etat["Passed"] = nbr_qc_passed

            # print(f"resume_etat : {resume_etat}")

            dict_etat[etude.nom] = resume_etat
            # print(f"dict_etat : {dict_etat}")

    # Enregistrement du log-----------------------------------
    # --------------------------------------------------------
    nom_documentaire = " Affiche la page graphique"
    information_log(request, nom_documentaire)
    # --------------------------------------------------------
    # --------------------------------------------------------

    tab_list = {}
    derniers_uploads = []
    # Savoir si des étapes se nomment : téléchargement, download
    list_nom = ["téléchargement", "download", "Téléchargement", "Download", "Upload"]
    etapes_comprenant_le_nom_upload = RefEtapeEtude.objects.filter(nom__in=list_nom)
    # print(f"etapes_comprenant_le_nom_upload : {etapes_comprenant_le_nom_upload}")

    for etape in etapes_comprenant_le_nom_upload:
        id_etape = etape.id
        # etat = 1 correspond à l'étape "Nouveau"
        jonctions_etape_suivi = JonctionEtapeSuivi.objects.filter(etape=id_etape).filter(etat=1)
        print(f"jonctions_etape_suivi : {jonctions_etape_suivi}")

        for jonction in jonctions_etape_suivi:
            dict_object = {}
            # print(f"jonction.upload.id : {jonction.upload.id}")

            dossier_result = SuiviUpload.objects.filter(dossier=jonction.upload.id)
            # print(f"dossier result: {dossier_result}")
            if dossier_result.exists():
                dossier_first = dossier_result[0]
                date_ex = datetime.strftime(dossier_first.date_examen,'%Y-%m-%d')
                date_up = datetime.strftime(dossier_first.date_upload,'%Y-%m-%d')

                dict_object[dossier_first.id_patient] = {"id": dossier_first.id,
                                                        "nip": dossier_first.id_patient,
                                                        "date_exam": date_ex,
                                                        "date_upload": date_up,
                                                        "user": dossier_first.user.username,
                                                        }

                derniers_uploads.append([dossier_first.id_patient,
                                date_ex,date_up,
                                dossier_first.user.username,
                                ])
            
    creation_json = json.dumps(tab_list)

    print(f"dict_etat : {dict_etat}")
    print(f"derniers_uploads : {derniers_uploads}")

    return render(request, "admin_page.html", {"nbr_etat": dict_etat,
                                            "derniers_upload": derniers_uploads,
                                            'title_page':'Accueil Administration de l\'application Upload'
                                            })

    # return render(request, "admin_page.html", {"nbr_etat": dict_etat,
    #                                            "list_json": derniers_uploads,
    #                                            'title_page':'Accueil Administration de l\'application Upload'
    #                                            })
                                               #V1_ADMIN_STAT.html
