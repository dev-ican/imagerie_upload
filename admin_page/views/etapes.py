# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from admin_page.forms import FormsEtape, FormsEtapeEdit
from upload.models import (
    JonctionEtapeSuivi,
    RefEtapeEtude,
    RefEtudes,
    SuiviUpload,
)

from .module_admin import choice_etude
from .module_log import (
    creation_log,
    edition_log,
    information_log,
    suppr_log,
)

# Gère la partie Admin Etapes
# --------------------------------------------
# --------------------------------------------
# --------------------------------------------


@login_required(login_url="/auth/auth_in/")
def admin_etape(request):
    """Charge la page index pour l'ajout ou l'édition d'une étape."""
    liste_protocole = []
    if request.method == "POST":
        val_nom = request.POST["nom"]
        #val_etude = request.POST["etudes"]
        #query = RefEtudes.objects.get(id__exact=val_etude)
        RefEtapeEtude.objects.create(nom=val_nom) #etude=query)
        # Enregistrement du log--------------------------------
        # -----------------------------------------------------
        nom_documentaire = " a créé l'étape : " + val_nom
        creation_log(request, nom_documentaire)
        # -----------------------------------------------------
        # -----------------------------------------------------
    form = FormsEtape()
    #liste_protocole = choice_etude(True)
    #form.fields["etudes"].choices = liste_protocole
    #form.fields["etudes"].initial = [0]
    etape_tab = RefEtapeEtude.objects.all()
    return render(
        request,
        "admin_etapes.html",
        {"form": form, "resultat": etape_tab},
    )


@login_required(login_url="/auth/auth_in/")
def etape_edit(request, id_etape):
    """Charge la page d'édition des étapes."""
    liste_protocole = []
    if request.method == "POST":
        select_etape = RefEtapeEtude.objects.get(pk=id_etape)
        nom_edit = request.POST["nom"]
        etudes = request.POST["etudes"]
        ref_etude = RefEtudes.objects.get(id=etudes)
        # Enregistrement du log---------------------------------
        # ------------------------------------------------------
        nom_documentaire = (
            " a editer l'étape etape/etude - etude édité/etape édité : "
            + select_etape.nom
            + "/"
            + str(nom_edit)
        )
        edition_log(request, nom_documentaire)
        # ------------------------------------------------------
        # ------------------------------------------------------
        select_etape.nom = nom_edit
        select_etape.save()
        select_etape.etude.add(ref_etude)    #.user.add(user_info)
        #select_etape.etude = ref_etude
        form = FormsEtape()
        return HttpResponseRedirect("/admin_page/etapes/")
    else:
        etape_filtre = RefEtapeEtude.objects.get(id=id_etape)
        id_etude = RefEtudes.objects.get(pk=1)
        form = FormsEtapeEdit()
        liste_protocole = choice_etude(False)
        form.fields["etudes"].choices = liste_protocole
        form.fields["etudes"].initial = [0]
        form.fields["nom"].initial = etape_filtre.nom
        # Enregistrement du log-----------------------------
        # --------------------------------------------------
        nom_documentaire = (
            " a ouvert l'édition pour l'étape etude/etape : "
            + etape_filtre.nom
        )
        information_log(request, nom_documentaire)
        # --------------------------------------------------
        # --------------------------------------------------
    etape_tab = RefEtudes.objects.filter(refetapeetude__id=id_etape)
    return render(
        request,
        "admin_etapes_edit.html",
        {
            "form": form,
            "resultat": etape_tab,
            "select": int(id_etape),
        },
    )


@login_required(login_url="/auth/auth_in/")
def etape_del(request, id_etape):
    """Appel Ajax permettant la supression d'une étapes."""
    liste_protocole = []
    x = 0
    if request.method == "POST":
        suppr = True
        info_suivi = JonctionEtapeSuivi.objects.filter(
            etape__id__exact=id_etape
        )
        if info_suivi.exists():
            for nbr in info_suivi:
                x += 1
            suppr = False
        if suppr:
            id_log = RefEtapeEtude.objects.get(
                id__exact=id_etape
            )
            # Enregistrement du log------------------------------
            # ---------------------------------------------------
            nom_documentaire = (
                " a supprimé l'étude (etude/etape) : "
                + id_log.etude.nom
                + "/"
                + id_log.nom
            )
            suppr_log(request, nom_documentaire)
            # ---------------------------------------------------
            # ---------------------------------------------------
            RefEtapeEtude.objects.get(
                id__exact=id_etape
            ).delete()
            message = messages.add_message(
                request, messages.WARNING, "Suppression Faite"
            )
        else:
            id_log = RefEtapeEtude.objects.get(
                id__exact=id_etape
            )
            # Enregistrement du log------------------------------
            # ---------------------------------------------------
            nom_documentaire = (
                " à reçu un message d'erreur de suppression pour (etude/etape) : "
                + id_log.etude.nom
                + "/"
                + id_log.nom
            )
            information_log(request, nom_documentaire)
            # ----------------------------------------------
            # ----------------------------------------------
            message = messages.add_message(
                request,
                messages.WARNING,
                "Suppression annulée, cette étape est liée à :"
                + x
                + " suivi(s)",
            )
    form = FormsEtape()
    liste_protocole = choice_etude(True)
    form.fields["etudes"].choices = liste_protocole
    form.fields["etudes"].initial = [0]
    etape_tab = RefEtapeEtude.objects.all()
    context = {
        "form": form,
        "resultat": etape_tab,
        "message": message,
    }
    return render(request, "admin_etapes.html", context)

def link_del(request):
    id_etape = request.POST.get("val_user")
    id_etude = request.POST.get("type_tab")
    suppr = True
    info_suivi = SuiviUpload.objects.filter(etude__etude__id=id_etude)
    if info_suivi.exists():
        for nbr in info_suivi:
            x += 1
        suppr = False
    if suppr:
        id_log = RefEtapeEtude.objects.get(
            id__exact=id_etape
        )
        bdd_etape = RefEtapeEtude.objects.get(pk=id_etape)
        bdd_etude = RefEtudes.objects.get(pk=id_etude)

        bdd_etape.refetudes.remove(bdd_etude)

