# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from upload.models import Contact, RefTypeAction, Log

from .forms import ContactForm


@login_required(login_url="/auth/auth_in/")
def gestion_contact(request):
    """Affiche la page des contact, permet de récupérer les contact déjà
    présent et de les afficher."""
    form = ContactForm()
    contact_tab = Contact.objects.all()
    date_now = timezone.now()
    user_current = request.user
    type_action = RefTypeAction.objects.get(pk=4)
    Log.objects.create(user=user_current,
                       action=type_action,
                       date=date_now,
                       info="Visite des contacts",
                       )
    return render(request, "V1_CONTACT.html", {"resultat": contact_tab,
                                               "form": form
                                               })


@login_required(login_url="/auth/auth_in/")
def new_contact(request):
    """Permet de créer un nouveau contact."""
    if request.method == "POST":
        nom = request.POST["nom"]
        prenom = request.POST["prenom"]
        courriel = request.POST["email"]
        telephone = request.POST["telephone"]
        poste = request.POST["poste"]
        Contact.objects.create(
            nom=nom,
            prenom=prenom,
            courriel=courriel,
            telephone=telephone,
            poste=poste,
        )
    return redirect("/contact/")


@login_required(login_url="/auth/auth_in/")
def contact_edit(request, id):
    """Permet d'éditer un contact sélectionné."""
    if request.method == "POST":
        form = ContactForm()
        nom = request.POST["nom"]
        prenom = request.POST["prenom"]
        courriel = request.POST["email"]
        telephone = request.POST["telephone"]
        poste = request.POST["poste"]

        # Enregistrement du log------------------------------------------------------------------------
        # ---------------------------------------------------------------------------------------------
        date_now = timezone.now()
        user_current = request.user
        type_action = RefTypeAction.objects.get(pk=2)
        nom_documentaire = (
            "Edition du contact : "
            + str(nom)
            + " "
            + str(prenom)
            + "id: "
            + str(id)
        )
        Log.objects.create(
            user=user_current,
            action=type_action,
            date=date_now,
            info=nom_documentaire,
        )
        # ----------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------
        
        Contact.objects.filter(id=id).update(
            nom=nom,
            prenom=prenom,
            courriel=courriel,
            telephone=telephone,
            poste=poste,
        )
        return redirect("/contact/")
    else:
        obj = Contact.objects.get(id__exact=id)
        # Enregistrement du log------------------------------------------------------------------------
        # ---------------------------------------------------------------------------------------------
        date_now = timezone.now()
        user_current = request.user
        type_action = RefTypeAction.objects.get(pk=2)
        nom_documentaire = (
            "Affichage de l'édition du contact : "
            + str(obj.nom)
            + " "
            + str(obj.prenom)
        )
        Log.objects.create(
            user=user_current,
            action=type_action,
            date=date_now,
            info=nom_documentaire,
        )
        # ----------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------
        info = {
            "nom": obj.nom,
            "prenom": obj.prenom,
            "email": obj.courriel,
            "telephone": obj.telephone,
            "poste": obj.poste,
        }
        form = ContactForm(info)
    contact_tab = Contact.objects.all()
    return render(
        request,
        "V1_CONTACT_EDIT.html",
        {"form": form, "resultat": contact_tab, "select": int(id)},
    )


@login_required(login_url="/auth/auth_in/")
def contact_deleted(request, id):
    """Permet de supprimer un contact, utilise Ajax."""
    if request.method == "POST":
        var_suivi = Contact.objects.get(id=int(id))
        # Enregistrement du log------------------------------------------------------------------------
        # ---------------------------------------------------------------------------------------------
        date_now = timezone.now()
        user_current = request.user
        type_action = RefTypeAction.objects.get(pk=3)
        nom_documentaire = (
            "Suppression du contact : "
            + str(var_suivi.nom)
            + " "
            + str(var_suivi.prenom)
        )
        Log.objects.create(
            user=user_current,
            action=type_action,
            date=date_now,
            info=nom_documentaire,
        )
        # ----------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------
        var_suivi.delete()
        message = messages.add_message(
            request, messages.WARNING, "Suppression Faite"
        )
    form = ContactForm()
    contact_tab = Contact.objects.all()
    context = {"form": form, "resultat": contact_tab, "message": message}
    return render(request, "contact.html", context)
