from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .models import (DossierUpload, JonctionUtilisateurEtude,
                     RefControleQualite, RefEtapeEtude, RefEtatEtape,
                     RefEtudes, RefInfoCentre, RefTypeAction, SuiviDocument)


class TestApp(TestCase):
    """ Mise en place des tests """

    def setUp(self):
        """ Mise en place des bases de données """
        
        date_now = timezone.now()
        test_user1 = User.objects.create_user(username="testuser1",
                                              password="testtest"
                                              )
        test_user2 = User.objects.create_user(username="testuser2",
                                              password="testtest"
                                              )

        test_etude1 = RefEtudes.objects.create(nom="test_etude1",
                                               date_ouverture=date_now
                                               )
        test_etude2 = RefEtudes.objects.create(nom="test_etude2",
                                               date_ouverture=date_now
                                               )
 
        RefEtatEtape.objects.create(id=1,
                                    nom="test_etape"
                                    )

        JonctionUtilisateurEtude.objects.create(user=test_user1,
                                                etude=test_etude1,
                                                date_autorisation=date_now,
                                                )

        JonctionUtilisateurEtude.objects.create(user=test_user2,
                                                etude=test_etude2,
                                                date_autorisation=date_now,
                                                )

        etape_etude_01 = RefEtapeEtude.objects.create(nom="Etape_test1")
        etape_etude_01.etude.add(test_etude1)
        etape_etude_01.etude.add(test_etude2)
        etape_etude_01.save()

        etape_etude_02 = RefEtapeEtude.objects.create(nom="Etape_test2")
        etape_etude_02.etude.add(test_etude1)
        etape_etude_02.etude.add(test_etude2)
        etape_etude_02.save()

        test_centre_01 = RefInfoCentre.objects.create(nom="Centre_test1",
                                                   numero="125",
                                                   date_ajout=date_now
                                                   )
        test_centre_01.user.add(test_user1)
        test_centre_01.save()

        test_centre_02 = RefInfoCentre.objects.create(nom="Centre_test2",
                                                   numero="32",
                                                   date_ajout=date_now
                                                   )
        test_centre_02.user.add(test_user2)
        test_centre_02.save()

        qc_insert = RefControleQualite.objects.create(nom="QC_test")
        qc_insert.save()

        create_dossier = DossierUpload.objects.create(user=test_user1,
                                                      controle_qualite=qc_insert,
                                                      date=date_now
                                                      )
        create_dossier.save()

        doc_1 = SuiviDocument.objects.create(user=test_user1,
                                             etude=test_etude2,
                                             titre="Test_doc",
                                             description="Desc_Test_Doc",
                                             date=date_now,
                                             fichiers="",
                                             background="bg-nw-protocole.jpg",
                                             )
        doc_1.save()

        RefTypeAction.objects.create(id=1, nom="Action_1")
        RefTypeAction.objects.create(id=2, nom="Action_2")
        RefTypeAction.objects.create(id=3, nom="Action_3")
        RefTypeAction.objects.create(id=4, nom="Action_4")
        RefTypeAction.objects.create(id=5, nom="Action_5")
        RefTypeAction.objects.create(id=6, nom="Action_6")
        RefTypeAction.objects.create(id=7, nom="Action_7")

    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------
    # TEST FORMULAIRE MODULE
    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------

    def test_upload(self):
        """Test le module formulaire d'upload"""

        c = Client()

        date_now = timezone.now()
        c.login(username="testuser1", password="testtest")
        response = c.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")

        get_form = c.get(reverse("formulaire"))
        self.assertEqual(get_form.status_code, 200)
        self.assertTemplateUsed(get_form, "V1_FORMULAIRE.html")

        id_user = User.objects.all()
        id_etude = JonctionUtilisateurEtude.objects.all()
        id_etape = RefEtatEtape.objects.get(id__exact=1)
        val_dict = {
            "user_current": id_user[0],
            "etudes": id_etude[0].id,
            "nip": "Test_upload",
            "date_irm": date_now,
            "id_etape": id_etape,
        }

        post_form = c.post(reverse("formulaire"), data=val_dict)
        self.assertEqual(post_form.status_code, 302)
        self.assertTemplateUsed(get_form, "V1_FORMULAIRE.html")
