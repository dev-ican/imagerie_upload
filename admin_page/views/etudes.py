from django.shortcuts import render
from django.http import (
    HttpResponseRedirect
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .module_views import *
from .module_log import *

from django.utils import timezone

from admin_page.forms import (
    FormsEtude
)
from upload.models import (
    RefEtudes,
    RefEtapeEtude,
    JonctionEtapeSuivi
)

# Gère la partie Admin Etudes
# ----------------------------------------------------------------
# ----------------------------------------------------------------
# ----------------------------------------------------------------


@login_required(login_url="/auth/auth_in/")
def adminetude(request):
    """ Charge la page index pour l'ajout ou l'édition d'une étude """
    if request.method == "POST":
        nom = request.POST["nom"]
        date_now = timezone.now()
        RefEtudes.objects.create(nom=nom, date_ouverture=date_now)
        # Enregistrement du log------------------------------------
        # ---------------------------------------------------------
        nom_documentaire = " a créé l'étude : " + nom
        creationLog(request, nom_documentaire)
        # ---------------------------------------------------------
        # ---------------------------------------------------------
    form = FormsEtude()
    etude_tab = RefEtudes.objects.all()
    return render(
        request,
        "admin_etude.html",
        {"form": form, "resultat": etude_tab},
    )


@login_required(login_url="/auth/auth_in/")
def etudeEdit(request, id_etape):
    """ Charge la page d'édition des études """
    if request.method == "POST":
        form = FormsEtude()
        nom = request.POST["nom"]
        date = request.POST["date_ouverture"]
        user_info = RefEtudes.objects.get(pk=id_etape)
        # Enregistrement du log-------------------------------
        # ----------------------------------------------------
        nom_documentaire = (
            " a editer l'étude id/nom/nouveau nom : "
            + str(id_etape)
            + "/"
            + user_info.nom
            + "/"
            + nom
        )
        editionLog(request, nom_documentaire)
        # ----------------------------------------------------
        # ----------------------------------------------------
        user_info.nom = nom
        user_info.date_ouverture = date
        user_info.save()
        return HttpResponseRedirect("/admin_page/etudes/")
    else:
        user_info = RefEtudes.objects.get(pk=id_etape)
        info = {
            "nom": user_info.nom,
            "date": user_info.date_ouverture,
        }
        form = FormsEtude(info)
        # Enregistrement du log------------------------------------------------------------------------
        # ---------------------------------------------------------------------------------------------
        nom_documentaire = (
            " a ouvert l'édition pour l'étude id/nouveau nom : "
            + str(id_etape)
            + "/"
            + user_info.nom
        )
        informationLog(request, nom_documentaire)
        # ----------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------
    etude_tab = RefEtudes.objects.all().order_by("nom")
    return render(
        request,
        "admin_etude_edit.html",
        {
            "form": form,
            "resultat": etude_tab,
            "select": int(id_etape),
        },
    )


@login_required(login_url="/auth/auth_in/")
def etudeDel(request, id_etape):
    """ Appel Ajax permettant la supression d'une étude """
    x = 0
    if request.method == "POST":
        info_etape = RefEtapeEtude.objects.filter(etude__id=id_etape)
        if info_etape.exists():
            for item in info_etape:
                info_suivi = JonctionEtapeSuivi.objects.filter(
                    etape=item.id
                )
                if info_suivi.exists():
                    x += 1
                    suppr = False
            if x == 0:
                suppr = True
        else:
            suppr = True
        if suppr == True:
            id_log = RefEtudes.objects.get(id=id_etape)
            # Enregistrement du log------------------------------------------------------------------------
            # ---------------------------------------------------------------------------------------------
            nom_documentaire = (
                " a supprimé l'étude (id/nom) : "
                + str(id_log.id)
                + "/"
                + str(id_log.nom)
            )
            supprLog(request, nom_documentaire)
            # ----------------------------------------------------------------------------------------------
            # ---------------------------------------------------------------------------------------------
            RefEtudes.objects.get(id=id_etape).delete()
            message = messages.add_message(
                request, messages.WARNING, "Suppression Faite"
            )
        else:
            id_log = RefEtudes.objects.get(id=id_etape)
            # Enregistrement du log------------------------------------------------------------------------
            # ---------------------------------------------------------------------------------------------
            nom_documentaire = (
                " a reçu un message d'erreur de suppression pour (id/nom) : "
                + str(id_log.id)
                + "/"
                + id_log.nom
            )
            informationLog(request, nom_documentaire)
            # ----------------------------------------------------------------------------------------------
            # ---------------------------------------------------------------------------------------------
            message = messages.add_message(
                request,
                messages.WARNING,
                "Suppression annulée, cette étude est liée à :"
                + x
                + " suivi(s)",
            )
    form = FormsEtude()
    etude_tab = RefEtudes.objects.all().order_by("nom")
    context = {
        "form": form,
        "resultat": etude_tab,
        "message": message,
    }
    return render(request, "admin_etude.html", context)
