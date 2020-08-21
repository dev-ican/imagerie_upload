from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from upload.models import SuiviUpload, JonctionUtilisateurEtude, JonctionEtapeSuivi, RefControleQualite, RefEtudes, RefInfocentre, RefEtapeEtude, RefEtatEtape

import requests
import json
import unicodedata

class Command(BaseCommand):
     def handle(self, *args, **options):

        # Renseigner la base User
        if User.objects.filter(pk=44).exists():
            test_user1 = User.objects.get(pk=44)
            test_user2 = User.objects.get(pk=45)
            test_user3 = User.objects.get(pk=46)
        else:
            test_user1 = User.objects.create_user(username="user1", password='testtest')
            test_user2 = User.objects.create_user(username="user2", password='testtest')
            test_user3 = User.objects.create_user(username="user3", password='testtest')

            test_user1.save()
            test_user2.save()
            test_user3.save()

        #Reigner les études

        if not RefEtudes.objects.filter(pk=1).exists():

            etude = RefEtudes.objects.create(
                    nom="etude1",
                    date_ouverture="2020-08-20")
            etude.save()
            etude = RefEtudes.objects.create(
                    nom="etude2",
                    date_ouverture="2020-08-20")
            etude.save()
            etude = RefEtudes.objects.create(
                    nom="etude3",
                    date_ouverture="2020-08-20")
            etude.save()
            etude = RefEtudes.objects.create(
                    nom="etude4",
                    date_ouverture="2020-08-20")
            etude.save()

        #Renseigner les etat

        if not RefEtatEtape.objects.filter(pk=1).exists():
            etat = RefEtatEtape.objects.create(
                    nom="En cours")
            etat.save()
            etat = RefEtatEtape.objects.create(
                    nom="Erreur")
            etat.save()
            etat = RefEtatEtape.objects.create(
                    nom="Demandes d'informations")
            etat.save()
            etat = RefEtatEtape.objects.create(
                    nom="Terminé")
            etat.save()

        #Renseigne les étapes des différentes études

        if not RefEtapeEtude.objects.filter(pk=1).exists():
            etape = RefEtapeEtude.objects.create(
                nom="Baseline_MRI",
                etude=RefEtudes.objects.get(pk=1))
            etape.save()

            etape = RefEtapeEtude.objects.create(
                nom="Baseline_Angiogram",
                etude=RefEtudes.objects.get(pk=1))
            etape.save()

            etape = RefEtapeEtude.objects.create(
                nom="End_of_treatment_MRI",
                etude=RefEtudes.objects.get(pk=1))
            etape.save()

            etape = RefEtapeEtude.objects.create(
                nom="Unscheduled_MRI",
                etude=RefEtudes.objects.get(pk=1))
            etape.save()

            etape = RefEtapeEtude.objects.create(
                nom="Exemple_etape1",
                etude=RefEtudes.objects.get(pk=2))
            etape.save()

            etape = RefEtapeEtude.objects.create(
                nom="Exemple_etape2",
                etude=RefEtudes.objects.get(pk=2))
            etape.save()

            etape = RefEtapeEtude.objects.create(
                nom="Exemple_etape3",
                etude=RefEtudes.objects.get(pk=2))
            etape.save()

            etape = RefEtapeEtude.objects.create(
                nom="Exemple_etape4",
                etude=RefEtudes.objects.get(pk=2))
            etape.save()

        #Renseigne les jonctions entre étude et utilisateurs

        if not JonctionUtilisateurEtude.objects.filter(pk=1).exists():
            j_etude_util = JonctionUtilisateurEtude.objects.create(
                user=test_user1,
                etude=RefEtudes.objects.get(pk=1),
                date_autorisation="2020-08-20")
            j_etude_util.save()

            j_etude_util = JonctionUtilisateurEtude.objects.create(
                user=test_user2,
                etude=RefEtudes.objects.get(pk=2),
                date_autorisation="2020-08-20")
            j_etude_util.save()

            j_etude_util = JonctionUtilisateurEtude.objects.create(
                user=test_user2,
                etude=RefEtudes.objects.get(pk=1),
                date_autorisation="2020-08-20")
            j_etude_util.save()

        #Renseigne les info du centre liée à l'utilisateur

        if not RefInfocentre.objects.filter(pk=1).exists():
            info = RefInfocentre.objects.create(
                nom="Nom_centre1",
                numero="001",
                date_ajout="2020-08-20",
                user=test_user1)
            info.save()

            info = RefInfocentre.objects.create(
                nom="Nom_centre3",
                numero="003",
                date_ajout="2020-08-20",
                user=test_user2)
            info.save()

            info = RefInfocentre.objects.create(
                nom="Nom_centre2",
                numero="002",
                date_ajout="2020-08-20",
                user=test_user3)
            info.save()

        #Renseigne les controles qualités

        if not RefControleQualite.objects.filter(pk=1).exists():
            qc = RefControleQualite.objects.create(
                nom="QC passed")
            qc.save()

            qc = RefControleQualite.objects.create(
                nom="QC refused")
            qc.save()

        #Renseigne un suivi upload

        if not SuiviUpload.objects.filter(pk=1).exists():
            upload = SuiviUpload.objects.create(
                user=test_user1,
                etude=JonctionUtilisateurEtude.objects.get(pk=1),
                id_patient="0001256",
                date_upload="2020-08-20",
                date_examen="2020-08-20",
                controle_qualite=RefControleQualite.objects.get(pk=1))
            upload.save()

            upload = SuiviUpload.objects.create(
                user=test_user1,
                etude=JonctionUtilisateurEtude.objects.get(pk=1),
                id_patient="00002589",
                date_upload="2020-08-20",
                date_examen="2020-08-20",
                controle_qualite=RefControleQualite.objects.get(pk=2))
            upload.save()   

            upload = SuiviUpload.objects.create(
                user=test_user1,
                etude=JonctionUtilisateurEtude.objects.get(pk=1),
                id_patient="000025893",
                date_upload="2020-08-20",
                date_examen="2020-08-20",
                controle_qualite=RefControleQualite.objects.get(pk=1))
            upload.save()

        #Renseigne les etat des étapes des suivis

        if not JonctionEtapeSuivi.objects.filter(pk=1).exists():
            etat_etape = JonctionEtapeSuivi.objects.create(
                upload=SuiviUpload.objects.get(pk=1),
                etape=RefEtapeEtude.objects.get(pk=1),
                etat=RefEtatEtape.objects.get(pk=1),
                date="2020-08-20")
            etat_etape.save()

            etat_etape = JonctionEtapeSuivi.objects.create(
                upload=SuiviUpload.objects.get(pk=2),
                etape=RefEtapeEtude.objects.get(pk=1),
                etat=RefEtatEtape.objects.get(pk=2),
                date="2020-08-20")
            etat_etape.save()
                                   

        self.stdout.write(self.style.SUCCESS('commande succes'))