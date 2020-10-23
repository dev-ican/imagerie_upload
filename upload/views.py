from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import UploadForm
from .models import (
    JonctionUtilisateurEtude,
    SuiviUpload,
    RefControleQualite,
    JonctionEtapeSuivi,
    DossierUpload,
    RefEtatEtape,
    RefEtapeEtude,
    SuiviDocument,
    log,
    RefTypeAction,
)

from django.utils import timezone
import zipfile
import os

# Create your views here.


@login_required(login_url="/auth/auth_in/")
def index(request):
    date_now = timezone.now()
    user_current = request.user
    doc_list = SuiviDocument.objects.all()
    type_action = RefTypeAction.objects.get(pk=4)
    log.objects.create(
        user=user_current,
        action=type_action,
        date=date_now,
        info="Visite de l'index",
    )

    return render(
        request,
        "index.html",
        {"response": doc_list, "user": user_current},
    )


@login_required(login_url="/auth/auth_in/")
def contact(request):
    date_now = timezone.now()
    user_current = request.user
    type_action = RefTypeAction.objects.get(pk=4)
    log.objects.create(
        user=user_current,
        action=type_action,
        date=date_now,
        info="Visite des contacts",
    )
    return render(request, "contact.html")


@login_required(login_url="/auth/auth_in/")
def formulaire(request):
    date_now = timezone.now()
    user_current = request.user
    liste_protocole = []
    if request.method == "POST":
        type_action = RefTypeAction.objects.get(pk=4)
        log.objects.create(
            user=user_current,
            action=type_action,
            date=date_now,
            info="Utilisation du formulaire pour envois de donnée",
        )
        etude = request.POST["etudes"]
        nip = request.POST["nip"]
        date = request.POST["date_irm"]
        id_etude = JonctionUtilisateurEtude.objects.get(
            id__exact=etude
        )
        id_qc = RefControleQualite.objects.get(id=1)
        id_etape = RefEtatEtape.objects.get(id=1)
        id_etapes = RefEtapeEtude.objects.filter(
            etude=id_etude.etude.id
        )
        date_now = timezone.now()
        filez = request.FILES.getlist("upload")
        create_jonction = DossierUpload(
            user=user_current, controle_qualite=id_qc, date=date
        )
        create_jonction.save()
        for f in filez:
            create_suivi = SuiviUpload(
                user=user_current,
                etude=id_etude,
                id_patient=nip,
                date_upload=date_now,
                date_examen=date,
                fichiers=f,
                dossier=create_jonction,
            )
            name_file = f.name
            create_suivi.save()
            if name_file.find(".zip"):
                zipfile_save = zipfile.ZipFile(
                    create_suivi.fichiers.path, mode="r"
                )
                path = os.path.dirname(create_suivi.fichiers.path)
                zipfile_save.extractall(path)
                zipfile_save.close()
                if os.path.exists(create_suivi.fichiers.path):
                    os.remove(create_suivi.fichiers.path)
        for etape in id_etapes:
            create_etape = JonctionEtapeSuivi.objects.create(
                upload=create_jonction, etape=etape, etat=id_etape
            )
        var_url = "/upload/form/"
        return redirect(var_url)
    form = UploadForm()
    request_utilisateur_protocole = (
        JonctionUtilisateurEtude.objects.filter(
            user=user_current.id
        )
    )
    for util_pro in request_utilisateur_protocole:
        collapse = (util_pro.id, util_pro.etude.nom)
        liste_protocole.append(collapse)
    liste_protocole.append((0, "Séléctionner une étude"))
    form.fields["etudes"].choices = liste_protocole
    form.fields["etudes"].initial = [0]
    return render(request, "form_upload.html", {"form": form})
