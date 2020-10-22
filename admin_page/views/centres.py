from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .module_views import *
from .module_log import *
from django.utils import timezone
from admin_page.forms import FormCentre
from upload.models import (
    RefInfocentre,
    SuiviUpload
)

# Gère la partie Admin Centres
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------


@login_required(login_url="/auth/auth_in/")
def admincentre(request):
    """ Charge la page index pour l'ajout ou l'édition d'un centre """
    if request.method == "POST":
        nom = request.POST["nom"]
        numero = request.POST["numero"]
        date_now = timezone.now()
        nw_centre = RefInfocentre.objects.create(
            nom=nom, numero=numero, date_ajout=date_now
        )
        # Enregistrement du log---------------------------------------
        # ------------------------------------------------------------
        nom_documentaire = (
            " a créé le centre : " + nw_centre.nom + nw_centre.numero
        )
        creationLog(request, nom_documentaire)
        # ------------------------------------------------------------
        # ------------------------------------------------------------
    form = FormCentre()
    centre_tab = RefInfocentre.objects.all().order_by("nom")
    return render(
        request,
        "admin_centre.html",
        {"form": form, "resultat": centre_tab},
    )


@login_required(login_url="/auth/auth_in/")
def centreEdit(request, id_etape):
    """ Charge la page d'édition des centres """
    if request.method == "POST":
        form = FormCentre()
        nom = request.POST["nom"]
        numero = request.POST["numero"]
        user_info = RefInfocentre.objects.get(pk=id_etape)
        # Enregistrement du log------------------------------
        # ---------------------------------------------------
        nom_documentaire = (
            " a editer le centre : "
            + str(user_info.nom)
            + str(user_info.numero)
            + " (Nouvelle entrée : "
            + str(nom)
            + str(numero)
            + ")"
        )
        editionLog(request, nom_documentaire)
        # ----------------------------------------------------
        # ----------------------------------------------------
        user_info.nom = nom
        user_info.numero = numero
        user_info.save()
        return HttpResponseRedirect("/admin_page/centre/")
    else:
        user_info = RefInfocentre.objects.get(pk=id_etape)
        info = {
            "nom": user_info.nom,
            "numero": user_info.numero,
            "date_ajout": user_info.date_ajout,
        }
        form = FormCentre(info)
        # Enregistrement du log------------------------------------------------------------------------
        # ---------------------------------------------------------------------------------------------
        nom_documentaire = (
            " a ouvert l'édition pour le centre : "
            + str(user_info.nom)
            + str(user_info.numero)
        )
        informationLog(request, nom_documentaire)
        # ----------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------
    centre_tab = RefInfocentre.objects.all().order_by("nom")
    return render(
        request,
        "admin_centre_edit.html",
        {
            "form": form,
            "resultat": centre_tab,
            "select": int(id_etape),
        },
    )


@login_required(login_url="/auth/auth_in/")
def centreDel(request, id_etape):
    """ Appel Ajax permettant la supression d'un centre """
    x = 0
    if request.method == "POST":
        suppr = True
        info_centre = RefInfocentre.objects.get(id__exact=id_etape)
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
            supprLog(request, nom_documentaire)
            # -------------------------------------------------------
            # -------------------------------------------------------
            RefInfocentre.objects.get(id__exact=id_etape).delete()
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
            informationLog(request, nom_documentaire)
            # --------------------------------------------------------
            # --------------------------------------------------------
    form = FormCentre()
    centre_tab = RefInfocentre.objects.all().order_by("nom")
    context = {
        "form": form,
        "resultat": centre_tab,
        "message": message,
    }
    return render(request, "admin_centre.html", context)
