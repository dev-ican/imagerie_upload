# -*-coding:Utf-8 -*

""" Ce fichier permet de gérer les modules de l'application
 faisant partie du menus administration"""

from upload.models import (
    RefEtudes,
    RefInfocentre,
)


def checkmdp(first, second):
    check = False
    if len(first) > 0 and len(second) > 0:
        if first == second:
            check = True

    return check


def take_data(etude, centre):

    list_response = []
    if etude != "EMPTY":
        etude = int(etude) + 1
        save_etude = RefEtudes.objects.get(pk=etude)
        list_response.append(save_etude)
    else:
        list_response.append("null")

    if centre != "EMPTY":
        save_centre = RefInfocentre.objects.get(pk=centre)
        list_response.append(save_centre)
    else:
        list_response.append("null")

    return list_response


def choiceEtude(val_zero):
    liste_etude = []
    request_etude = RefEtudes.objects.all()

    for util_pro in enumerate(request_etude):
        collapse = (util_pro[1].id, util_pro[1].nom)
        liste_etude.append(collapse)

    if val_zero:
        liste_etude.append((0, "Séléctionner une étude"))

    return liste_etude


def choiceCentre(val_zero):
    liste_centre = []
    request_centre = RefInfocentre.objects.all().order_by("nom")

    for util_pro in enumerate(request_centre):
        collapse = (util_pro[1].id, util_pro[1].nom)
        liste_centre.append(collapse)

    if val_zero:
        liste_centre.append((0, "Sélectionner un centre"))
    return liste_centre
