# -*-coding:Utf-8 -*

from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from upload.models import (DossierUpload, JonctionEtapeSuivi,
                           JonctionUtilisateurEtude, RefEtapeEtude, RefEtudes,
                           RefInfoCentre, SuiviUpload, ValideCompte,JonctionEtapeSuivi,RefEtatEtape)
from configparser import ConfigParser
from .module_log import suppr_log
from django.utils import timezone
from django.core.mail import EmailMessage

import ast


def gestion_etape(dict_etape_nom, dict_etape_value, nbr_etape, id_dossier, etude_select):
    """Ce module permet de ramener le nom de l'étape s'il y a une erreur,
    c'est indiqué à la place de l'étape."""
    # print(dict_etape_nom, dict_etape_value, nbr_etape, id_dossier, etude_select)
    
    if (len(dict_etape_nom) == 0 or len(dict_etape_value) != nbr_etape):
        element_etape = RefEtapeEtude.objects.filter(etude=etude_select.etude.etude)

        for item_info_etape in element_etape:
            nbr_etat = RefEtatEtape.objects.get(id=1)
            id_dossierupload = DossierUpload.objects.get(id=id_dossier.dossier.id)
            check_etape = JonctionEtapeSuivi.objects.filter(upload=id_dossierupload.id).filter(etape=item_info_etape.id)
            if not check_etape.exists():
                nw_etape = JonctionEtapeSuivi(upload=id_dossierupload, etape=item_info_etape, etat=nbr_etat)
                nw_etape.save()
        dictupload = info_upload(id_dossier)
        infoetape = infos_etats_etape(id_dossier)
        error = False
        return [error, infoetape]

    else:
        etape_etude = dict_etape_value
        error = False
        return [error, etape_etude]

# ancien nom : etude_recente
def centres_etude_selectionnee(dossiers_suiviupload):
    """renvoi les centres liès à l'étude selectionnée."""
    # print(f"dossiers01 : {dossiers}")
    centres = []
    
    try:
        for dossier_suiviupload in dossiers_suiviupload:
            centre = RefInfoCentre.objects.get(user=dossier_suiviupload.user.id)
            # print(f"centre01 : {centre}")
            if centre not in centres:
                centres.append(centre)

    except ObjectDoesNotExist:
        indic_error = "erreur"
    return centres


def etude_tris(dossiers):
    """Ce module renvoi les centres liés aux dossiers uploadés."""

    list_centre = []
    for dossier in dossiers:
        try:
            centre = RefInfoCentre.objects.get(user=dossier.user.id)
            if centre not in list_centre:
                list_centre.append(centre)

        except ObjectDoesNotExist:
            indic_error = "erreur"

    return list_centre


# def gestion_etude_recente(etude_recente, dossier_all, list_centre):
def gestion_etude_selectionnee(etude_selectionnee, centres):
    """Renvoi une liste comprenant  """

    etudes = RefEtudes.objects.all()
    infos_etude = []
    infos_centre = []
    # print(f'centres: {centres}')

    for centre in centres:
        dict_centre = {}
        dict_centre["id"] = centre.id
        dict_centre["nom"] = str(centre.nom) + str(centre.numero)
        infos_centre.append(dict_centre)

    for etude in etudes:
        dict_etude = {}

        try:
            etude_selectionnee_id = etude_selectionnee.etude.etude.id
        except:
            etude_selectionnee_id = -1

        if etude.id == etude_selectionnee_id:
            dict_etude["id"] = str(etude.id)
            dict_etude["option"] = "selected"
            dict_etude["nom"] = etude.nom
            infos_etude.append(dict_etude)
        else:
            dict_etude["id"] = str(etude.id)
            dict_etude["option"] = ""
            dict_etude["nom"] = etude.nom
            infos_etude.append(dict_etude)

    return [infos_centre, infos_etude]


def gestion_etude_tris(etude_change, dossier_all, list_centre):
    list_etude = RefEtudes.objects.all()
    str_etude = []
    str_centre = []
    str_dict = {}

    for centre in list_centre:

        str_dict_centre = {}
        str_dict_centre["id"] = centre.id
        str_dict_centre["nom"] = str(centre.nom) + str(
            centre.numero
        )
        str_centre.append(str_dict_centre)

    for etude in list_etude:
        str_dict = {}
        if etude.id == etude_change.id:
            str_dict["id"] = str(etude.id)
            str_dict["option"] = "selected"
            str_dict["nom"] = etude.nom
            str_etude.append(str_dict)
        else:
            str_dict["id"] = str(etude.id)
            str_dict["option"] = ""
            str_dict["nom"] = etude.nom
            str_etude.append(str_dict)
    return [str_centre, str_etude]


def info_upload(suivi_upload):
    """
    Cette fonction renvoi un dictionnaire contenant les informations liées a un fichier uploadé.
    La paramètre "suivi_upload" est un objet "SuiviUpload"
    """
    # Variable indiquant le nombre de fichiers (a supprimer)
    nbr_de_fichiers = SuiviUpload.objects.filter(dossier=suivi_upload.dossier.id).count()

    # Variable contenant l'objet "SuiviUpload" lié au paramètre suivi_upload
    nom_de_l_etude = SuiviUpload.objects.filter(dossier=suivi_upload.dossier.id)
    # nom_de_l_etude = SuiviUpload.objects.filter(dossier=suivi_upload.dossier.id)[:1]

    # var_qc contient l'objet "Dossier Upload" en lien avec suivi_upload
    var_qc = DossierUpload.objects.get(id=nom_de_l_etude[0].dossier.id)
    
    infos_upload = {}
    infos_upload["id_"] = suivi_upload.id
    infos_upload["Etudes"] = var_qc.controle_qualite.nom
    infos_upload["Etudes_id"] = var_qc.id
    infos_upload["id_patient"] = nom_de_l_etude[0].id_patient
    # infos_upload["nbr_upload"] = nbr_de_fichiers

    return infos_upload

# ancien nom : info_etape
def infos_etats_etape(dossier):
    """Renvoi les infos des états liées à une étape."""
    etapes = JonctionEtapeSuivi.objects.filter(upload=dossier.dossier.id).order_by("etape")
    # print(f"etape : {etapes}")
    infos_etats = []

    for etape in etapes:
        # Si l'état de l'étape est "En cours d'informations"
        if etape.etat.id == 4:
            infos_etats.append({"val_item": etape.date,
                                "etape_id": etape.id,
                                "en_cours_d_informations": True,
                                })
        else:
            infos_etats.append({"val_item": etape.etat.nom,
                                "etape_id": etape.id,
                                "en_cours_d_informations": False,
                                })                              
    return infos_etats


def nom_etape(etude_recente):
    """ce module renvoi le nom de l'étape récente."""
    nom_etape = RefEtapeEtude.objects.filter(etude=etude_recente)
    dict_etape_nom = []

    for nom in nom_etape:
        dict_etape_nom.append(nom.nom)
    return dict_etape_nom


def nom_etape_tris(etude_change):
    """ce module donne le nom des étapes de l'étude récente."""
    nom_etape = RefEtapeEtude.objects.filter(etude=etude_change)
    dict_etape_nom = []

    for nom in nom_etape:
        dict_etape_nom.append(nom.nom)
    return dict_etape_nom


def send_mail(user_send, compte, to_mail, origin):
    ''' Gère l'envois de courriel lors du processus de validation d'un compte'''
    # origin représente l'origine de la demande : Vérification pour une demande d'ouverture de compte venant d'un admin service
    # valider pour un compte validé par un admin SI
    # refus pour un compte refusé par un admin SI
    # Il faut poursuivre l'utilisation d'un document annexe pour le contenue texte.
    if origin == 'verification':
        title = str(user_send) + " demande la validation du compte " + str(compte.username)
        corps = "Bonjour, \n\n Une demande de validation de compte sur l'application d'upload est demandé par : " + str(user_send)
        corps += "\n\n Vous pouvez vous rendre sur l'application web Upload via ce lien : https://134.157.204.80/admin_page/authacc \n"
        corps += "\n CE COURRIEL EST UN MAIL AUTOMATIQUE MERCI DE NE PAS REPONDRE \n"
        corps += "\n Système app upload"
    elif origin == 'valider':
        title = str(user_send) + " vient de valider le compte : " + str(compte.username)
        corps = "Bonjour, \n\n Le compte en attente de validation " + str(compte.username) + " vient d'être validé par : " + str(user_send)
        corps += "\n\n Si vous avez une question sur cette validation, vous pouvez joindre le service SI par ce courriel : support_si@ican-institute.org \n"
        corps += "\n Vous pouvez vous rendre sur l'application web Upload via ce lien : https://134.157.204.80/admin_page/authacc \n"
        corps += "\n CE COURRIEL EST UN MAIL AUTOMATIQUE MERCI DE NE PAS REPONDRE \n"
        corps += "\n Système app upload"
    elif origin == 'refus':
        title = str(user_send) + " vient de REFUSER le compte : " + str(compte.username)
        corps = "Bonjour, \n\n Le compte en attente de validation " + str(compte.username) + " vient d'être refusé par : " + str(user_send)
        corps += "\n\n Si vous avez une question sur cette validation, vous pouvez joindre le service SI par ce courriel : support_si@ican-institute.org \n"
        corps += "\n Vous pouvez vous rendre sur l'application web Upload via ce lien : https://134.157.204.80/admin_page/authacc \n"
        corps += "\n CE COURRIEL EST UN MAIL AUTOMATIQUE MERCI DE NE PAS REPONDRE \n"
        corps += "\n Système app upload"
    email = EmailMessage(title, corps, 'app_upload@ican-institute.org', to=to_mail)
    email.send()


def send_rgpd_fail(user_stock, user_suppr, nip, to_mail):
    ''' Gère l'envois de courriel lors de la suppression de données après une indication de QC refused RGPD'''
    # user_stock représente l'utilisateur ayant déposé le patient
    # user_suppr représente l'utilisateur supprimant les données
    # nip représente le code utilisateur
    config = ConfigParser()		
    config.read("texte_app.ini",encoding="utf8")#read("texte_app.ini")
    mail_txt = config['mod_view']
    list_corp = ast.literal_eval(config.get("mod_view", "corp_rgpd"))

    to_mail = [to_mail]
    title = str(nip) + " " + mail_txt["title_rgpd"] + " " + str(user_suppr)
    corps = str(list_corp[0]) + \
        str(list_corp[1]) + \
        str(nip) + \
        str(list_corp[2]) + \
        str(list_corp[3]) + \
        str(list_corp[4]) + str(user_suppr) + "\n" + \
        str(list_corp[5]) + "\n\n" + \
        str(list_corp[6]) + "\n\n" + \
        str(list_corp[7])

    email = EmailMessage(title, corps, 'app_upload@ican-institute.org', to=to_mail)
    email.send()


def nw_password(check_mdp, type, nom, numero, username, pass_first, email):
    """Créé un password & un utilisateur"""
    if check_mdp:
        # Création de l'utilisateur après vérification de son mot de passe
        #__________________________________________________________________
        nw_user = User.objects.create_user(
                            username=username,
                            password=pass_first,
                            email=email,
                            is_active=False,
                            )
        # Sauvegarde du compte
        #_____________________
        nw_user.save()
        # Création du suivi du compte
        #___________________________
        nw_valide = ValideCompte.objects.create(create_user=nw_user,date_crea=timezone.now())
        # Sauvegarde de la création
        #_________________________
        nw_valide.save()
        # print(Group.objects.all())
        if int(type) == 0:
            my_group = Group.objects.get(name='Collaborateurs')
            my_group.user_set.add(nw_user)
        elif int(type) == 1:
            my_group = Group.objects.get(name='Utilisateurs')
            my_group.user_set.add(nw_user)
        elif int(type) == 2:
            my_group = Group.objects.get(name='Administrateur service')
            my_group.user_set.add(nw_user)

        nw_user.save()
        if len(nom) > 0 and len(numero) > 0:
            date_now = timezone.now()
            nw_centre = RefInfoCentre(
                nom=nom, numero=numero, date_ajout=date_now
            )
            nw_centre.save()
            nw_centre.user.add(nw_user)


def edit_password(
    check_mdp, type, username, pass_first, email, user_info
):
    """Ce module gère l'édition du mot de passe."""
    if check_mdp:
        user_info.username = username
        user_info.email = email
        user_info.set_password(pass_first)

        user_info.save()
    else:
        user_info.username = username
        user_info.email = email

    if int(type) == 0:
        user_info.is_staff = True
    else:
        if user_info.is_staff:
            user_info.is_staff = False
    user_info.save()


def pwd_nw(check_mdp, pass_first, email, user_info):
    """Ce module gère l'édition du mot de passe."""
    if check_mdp:
        user_info.email = email
        user_info.set_password(pass_first)
        user_info.save()


def jonc_centre(user_etude, etude, user_info, user_centre, centre):
    """Crée l'autorisation pour l'utilisateur vis à vis d'un centre."""
    if not user_etude.exists() and int(etude) > 0:
        date_now = timezone.now()
        save_etude = RefEtudes.objects.get(pk=etude)
        nw_jonction = JonctionUtilisateurEtude.objects.create(
            user=user_info,
            etude=save_etude,
            date_autorisation=date_now,
        )
    if not user_centre.exists() and int(centre) > 0:
        date_now = timezone.now()
        save_centre = RefInfoCentre.objects.get(pk=centre)
        save_centre.user.add(user_info)


def j_serial(o):
    """permet de sérialiser une date."""
    from datetime import date, datetime

    return (
        str(o).split(".")[0]
        if isinstance(o, (datetime, date))
        else None
    )


def del_auth(type_tab, id_search, req,user_info):
    """Ce module permet de supprimer une autorisation."""
    user_current = req.user
    message = ""
    if type_tab == "etude":
        user_etude = JonctionUtilisateurEtude.objects.get(
            id=id_search
        )
        verif_suivi = SuiviUpload.objects.filter(
            etude=user_etude
        )
        if not verif_suivi.exists():
            # Enregistrement du log---------------------------------
            # ------------------------------------------------------
            nom_documentaire = (
                " a supprimé l'autorisation : "
                + user_etude.etude.nom
                + " de l'utilisateur "
                + user_current.username
            )
            suppr_log(req, nom_documentaire)
            # -----------------------------------------------------
            # -----------------------------------------------------
            user_etude = JonctionUtilisateurEtude.objects.get(
                id__exact=id_search
            ).delete()
            user_etude.save()
            message = "Suppression des autorisations ont été appliquées"
        else:
            message = (
                "Suppression annulée, cet utilisateur à chargé des documents :"
                + str(len(verif_suivi))
                + " document(s) trouvés"
            )
    elif type_tab == "centre":
        user_type = User.objects.get(pk=user_info)
        verif = RefInfoCentre.objects.get(id=id_search)
        if verif:
            # Enregistrement du log--------------------------------
            # -----------------------------------------------------
            nom_documentaire = (
                " a supprimé l'autorisation : "
                + verif.nom
                + " de l'utilisateur "
                + user_current.username
            )
            suppr_log(req, nom_documentaire)
            # ----------------------------------------------------
            # ----------------------------------------------------
            verif.user.remove(user_type)
            message = (
                "Le centre n'est plus lié à cet utilisateur"
            )
        else:
            message = (
                "Cet utilisateur lié à ce centre a chargé des documents ("
                + str(len(verif))
                + " document(s))"
            )
    return message
