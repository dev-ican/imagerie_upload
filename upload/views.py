# -*- coding: utf-8 -*-

import os
import zipfile

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from django.core.exceptions import ObjectDoesNotExist
from .forms import UploadForm
from django.contrib import messages
from .models import (
    DossierUpload, JonctionEtapeSuivi, JonctionUtilisateurEtude,
    RefControleQualite, RefEtapeEtude, RefEtatEtape, RefTypeAction,
    SuiviDocument, SuiviUpload, Log, RefInfoCentre, RefEtudes)
from django.views.decorators.csrf import csrf_exempt, csrf_protect


@login_required(login_url="/auth/auth_in/")
def index(request):
    ''' Chargement de l'index, permet de charger
    les documents devant être listés sur la page d'accueil '''
    tab_etude = [] 
    date_now = timezone.now()
    user_current = request.user
    list_etude = JonctionUtilisateurEtude.objects.filter(user=user_current)
    for item in list_etude:
        tab_etude.append(item.etude.id)
    doc_list = SuiviDocument.objects.filter(etude__id__in=tab_etude)
    type_action = RefTypeAction.objects.get(pk=4)
    Log.objects.create(
        user=user_current,
        action=type_action,
        date=date_now,
        info="Visite de l'index",
    )

    return render(
        request,
        "V1_INDEX.html",
        {"response": doc_list, "user": user_current},
    )


@login_required(login_url="/auth/auth_in/")
def contact(request):
    '''Charge la page d'acceuil et
    renvois les contacts déjà entrés '''
    date_now = timezone.now()
    user_current = request.user
    type_action = RefTypeAction.objects.get(pk=4)
    Log.objects.create(user=user_current,
                      action=type_action,
                      date=date_now,
                      info="Visite des contacts",
                      )
    return render(request, "V1_CONTACT.html")


@login_required(login_url="/auth/auth_in/")
@csrf_exempt
def formulaire(request):
    ''' Charge la page du formulaire d'upload de fichier patient'''

    date_now = timezone.now()
    user_current = request.user
    liste_protocole = []
    
    if request.method == "POST":
        etude = request.POST["etudes"]
        nip = request.POST["nip"]
        date = request.POST["date_irm"]

        # --------------------------------------
        # --------------------------------------
        # Renseignement de la table de Log
        type_action = RefTypeAction.objects.get(pk=4)
        info_str = "Utilisation du formulaire pour envois de donnée pour l'ID patient : " + str(nip)
        log_info = Log(user=user_current,
                       action=type_action,
                       date=date_now,
                       info= str(info_str),
                      )
        log_info.save()
        # ---------------------------------------
        # ---------------------------------------

        id_etude = JonctionUtilisateurEtude.objects.get(id__exact=etude)
        id_qc = RefControleQualite.objects.get(id=1)
        id_etape = RefEtatEtape.objects.get(id=1)
        id_etapes = RefEtapeEtude.objects.filter(etude=id_etude.etude.id)
        date_now = timezone.now()
        filez = request.FILES.getlist("upload")
        # num_centre = RefInfoCentre.objects.get(user__exact=user_current.id)

        #TODO erreur lors de l'upload
        for centre in RefInfoCentre.objects.all():
            for user in centre.user.all():
                if user == request.user:
                    num_centre = RefInfoCentre.objects.get(user=user)
                    break


        if len(str(num_centre.numero)) == 3 :
            num_centre_val = str(num_centre.numero)
        elif len(str(num_centre.numero)) == 2:
            num_centre_val = "0" + str(num_centre.numero)
        elif len(str(num_centre.numero)) == 1:
            num_centre_val = "00" + str(num_centre.numero)
        
        nomage_id = str(id_etude.etude.nom) + "_" + num_centre_val + "_" + str(nip)

        # Vérification de la présence d'un id identique
        doublon = False
        try:
            search_doublon = SuiviUpload.objects.filter(id_patient__exact=nomage_id)
            if search_doublon.exists():
                doublon = True
        except ObjectDoesNotExist:
            doublon = False
        
        # Si un doublon est détecté rien n'est créé un message est renvoyé vers l'utilisateur
        if doublon == False:
            # Création du dossier en lien avec les fichiers chargés
            create_jonction = DossierUpload(user=user_current, controle_qualite=id_qc, date=date)
            create_jonction.save()

            # Création dans la table suivi upload de
            #chaque fichier chargé en lien avec le dossier
            for f in filez:
                create_suivi = SuiviUpload(user=user_current,
                                           etude=id_etude,
                                           id_patient=nomage_id,
                                           date_upload=date_now,
                                           date_examen=date,
                                           fichiers=f,
                                           dossier=create_jonction,
                                           )
                name_file = f.name
                create_suivi.save()

                # Si le fichier chargé est une archive alors décompréssé
                # MODIF 23112021 : Le fichier est décompréssé dans un dossier images hébergé dans Data
                # Medis doit aller chercher les nouveaux patient ainsi décompréssé dans ce dossier
                if name_file.find(".zip") != -1:
                    zipfile_save = zipfile.ZipFile(create_suivi.fichiers.path, mode="r")
                    path_save = "/home/koala/images_medis/" #os.getcwd() + "\data\images\\" + create_suivi.etude.etude.nom
                    path = str(path_save) + "/" + str(create_suivi.id_patient)
                    os.makedirs(path)
                    zipfile_save.extractall(path)
                    zipfile_save.close()
                    #if os.path.exists(create_suivi.fichiers.path):
                    #os.remove(create_suivi.fichiers.path)
                    
            # Création de chaque étapes pour le patient chargé
            for etape in id_etapes:
                JonctionEtapeSuivi.objects.create(upload=create_jonction,
                                                  etape=etape,
                                                  etat=id_etape
                                                  )
            var_url = "/form/"
            message = messages.add_message(request,
                                           messages.WARNING,
                                           "SUCCES - Vos données ont été chargées"
                                           )
            return redirect(var_url)
            
        elif doublon == True:
            var_url = "/form/"
            message = messages.add_message(request,
                                           messages.WARNING,
                                           "EREUR - Cet identifiant est déjà renseigné dans la base de donnée votre upload est annulé"
                                           )
            return redirect(var_url)

    list_log = SuiviUpload.objects.filter(user=user_current.id)
    # Charge le log de chargement de l'utilisateur actuel
    list_chargement = []
    for object in list_log:
        nip_chargement = [object.date_examen,object.etude.etude.nom,object.id_patient]
        list_chargement.append(nip_chargement)

    form = UploadForm()
    # Charge les listes déroulantes
    request_utilisateur_protocole = (JonctionUtilisateurEtude.objects.filter(user=user_current.id))

    for util_pro in request_utilisateur_protocole:
        collapse = (util_pro.id, util_pro.etude.nom)
        liste_protocole.append(collapse)
    
    liste_protocole.append((0, "Sélectionner une étude"))
    form.fields["etudes"].choices = liste_protocole
    form.fields["etudes"].initial = [0]

    return render(request, "V1_FORMULAIRE.html", {"form": form,
                                                  "log_upload": list_chargement
                                                  })
