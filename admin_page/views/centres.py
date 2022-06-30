# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from admin_page.forms import FormCentre, FormCentreEdit
from upload.models import RefInfoCentre, SuiviUpload

from .module_log import (
    creation_log,
    edition_log,
    information_log,
    suppr_log,
)

# Gère la partie Admin Centres
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------


@login_required(login_url="/auth/auth_in/")
def admin_centre(request):
    """Charge la page index pour l'ajout, l'édition ou la suppression d'un centre."""

    if request.method == "POST":
        nom = request.POST["nom"]
        numero = request.POST["numero"]
        date_now = timezone.now()
        nw_centre = RefInfoCentre.objects.create(nom=nom,
                                                 numero=numero,
                                                 date_ajout=date_now
                                                 )

        # Enregistrement du log---------------------------------------
        nom_documentaire = (" a créé le centre : "
                            + nw_centre.nom
                            + nw_centre.numero
                            )
        creation_log(request, nom_documentaire)
        # ------------------------------------------------------------
        
    form = FormCentre()
    # centres = RefInfoCentre.objects.all().order_by("nom")
    # resultat_info_centre = []
    # for centre in centres:
    #     alluser_centre = User.objects.filter(refinfocentre__id=centre.id)
    #     allinfo_suivi = SuiviUpload.objects.filter(user__in=alluser_centre).distinct("dossier").count()
    #     dict_info = {"nom":centre.nom,
    #                  "numero":centre.numero,
    #                  "date_ajout":centre.date_ajout,
    #                  "nbr":allinfo_suivi
    #                  }
    #     resultat_info_centre.append(dict_info)
    
    centre_query = RefInfoCentre.objects.all().order_by("nom")

    return render(request, "admin_centre.html", {"form": form,
                                                 "resultat": centre_query
                                                 })


@login_required(login_url="/auth/auth_in/")
def centre_edit(request, id_centre):
    """Charge la page d'édition des centres."""

    if request.method == "POST":
        form = FormCentre()
        nom = request.POST["nom"]
        numero = request.POST["numero"]
        date = request.POST["date_ajout"]
        centre_info = RefInfoCentre.objects.get(pk=id_centre)

        # Enregistrement du log------------------------------
        nom_documentaire = (" a editer le centre : "
                            + str(centre_info.nom)
                            + str(centre_info.numero)
                            + " (Nouvelle entrée : "
                            + str(nom)
                            + str(numero)
                            + ")"
                            )
        edition_log(request, nom_documentaire)
        # ----------------------------------------------------

        centre_info.nom = nom
        centre_info.numero = numero
        centre_info.date_ajout = date
        centre_info.save()
        return HttpResponseRedirect("/admin_page/centre/")

    else:
        """ demander à Vincent pour la sécurité, ici 'else' peut correspondre à GET, donc des informations à entrer dans l'url"""
        centre_info = RefInfoCentre.objects.get(pk=id_centre)
        format_date =centre_info.date_ajout.strftime('%Y-%m-%d')
        info = {"nom": centre_info.nom,
                "numero": centre_info.numero,
                "date_ajout": format_date,
                }
        form = FormCentreEdit(info)

        # Enregistrement du log------------------------------------------------------------------------
        # ---------------------------------------------------------------------------------------------
        nom_documentaire = (
            " a ouvert l'édition pour le centre : "
            + str(centre_info.nom)
            + str(centre_info.numero)
        )
        information_log(request, nom_documentaire)
        # ----------------------------------------------------------------------------------------------

    centre_tab = RefInfoCentre.objects.all().order_by("nom")
    return render(request, "admin_centre_edit.html", {"form": form,
                                                     "resultat": centre_tab,
                                                    #  "select": int(id_centre)
                                                     })


@login_required(login_url="/auth/auth_in/")
def centre_del(request, id_etape):
    """Appel Ajax permettant la supression d'un centre."""
    x = 0
    if request.method == "POST":
        suppr = True
        info_centre = RefInfoCentre.objects.get(
            id__exact=id_etape
        )
        info_user = User.objects.filter(
            refinfocentre__id__exact=info_centre.id
        )
        if info_user.exists():
            for item in info_user:
                info_suivi = SuiviUpload.objects.filter(
                    user__exact=item.id
                )
                if info_suivi.exists():
                    for nbr in info_suivi:
                        x += 1
                    suppr = False
        if suppr:
            # Enregistrement du log----------------------------------
            # -------------------------------------------------------
            nom_documentaire = (
                " a supprimé le centre : "
                + str(info_centre.nom)
                + str(info_centre.numero)
            )
            suppr_log(request, nom_documentaire)
            # -------------------------------------------------------
            # -------------------------------------------------------
            RefInfoCentre.objects.get(
                id__exact=id_etape
            ).delete()
            message = messages.add_message(
                request, messages.WARNING, "Suppression Faite"
            )
        else:
            message = messages.add_message(
                request,
                messages.WARNING,
                "Suppression annulée, cette étape est liée à :"
                + x
                + " suivi(s)",
            )
            # Enregistrement du log-----------------------------------
            # --------------------------------------------------------
            nom_documentaire = (
                " à reçu un message d'erreur de suppression pour le centre : "
                + info_centre.nom
                + info_centre.numero
            )
            information_log(request, nom_documentaire)
            # --------------------------------------------------------
            # --------------------------------------------------------
    form = FormCentre()
    centre_tab = RefInfoCentre.objects.all().order_by("nom")
    context = {
        "form": form,
        "resultat": centre_tab,
        "message": message,
    }
    return render(request, "admin_centre.html", context)
