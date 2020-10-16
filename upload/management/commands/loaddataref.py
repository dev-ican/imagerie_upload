from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from upload.models import SuiviUpload, JonctionUtilisateurEtude, JonctionEtapeSuivi, RefControleQualite, RefEtudes, RefInfocentre, RefEtapeEtude, RefEtatEtape, RefTypeAction

import requests
import json
import unicodedata

class Command(BaseCommand):
     def handle(self, *args, **options):

        if not RefTypeAction.objects.filter(pk=1).exists():
            etat = RefTypeAction.objects.create(
                    id=1, nom="Lecture")
            etat.save()
            etat = RefTypeAction.objects.create(
                    id=2, nom="Edition")
            etat.save()
            etat = RefTypeAction.objects.create(
                    id=3, nom="Suppression")
            etat.save()
            etat = RefTypeAction.objects.create(
                    id=4, nom="Informations")
            etat.save()
            etat = RefTypeAction.objects.create(
                    id=5, nom="Connexion")
            etat.save()
            etat = RefTypeAction.objects.create(
                    id=6, nom="Deconnexion")
            etat.save()
            etat = RefTypeAction.objects.create(
                    id=7, nom="Creation")
            etat.save()

        if not RefEtatEtape.objects.filter(pk=1).exists():
            etat = RefEtatEtape.objects.create(
                    id=1, nom="Nouveau")
            etat.save()
            etat = RefEtatEtape.objects.create(
                    id=2, nom="En cours")
            etat.save()
            etat = RefEtatEtape.objects.create(
                    id=3, nom="Erreur")
            etat.save()
            etat = RefEtatEtape.objects.create(
                    id=4, nom="Demandes d'informations")
            etat.save()
            etat = RefEtatEtape.objects.create(
                    id=5, nom="Terminé")
            etat.save()

        #Renseigne les controles qualités

        if not RefControleQualite.objects.filter(pk=1).exists():
            qc = RefControleQualite.objects.create(
                id=1, nom="new")
            qc.save()
            qc = RefControleQualite.objects.create(
                id=2, nom="QC passed")
            qc.save()
            qc = RefControleQualite.objects.create(
                id=3, nom="QC refused")
            qc.save()
                                   
        self.stdout.write(self.style.SUCCESS('commande succes'))