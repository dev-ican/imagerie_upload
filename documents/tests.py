from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from upload.models import (JonctionUtilisateurEtude, RefEtapeEtude,
                           RefEtatEtape, RefEtudes, RefInfocentre,
                           RefTypeAction, SuiviDocument)


class TestApp(TestCase):
    """ Mise en place des tests """

    def setUp(self):
        """ Mise en place des bases de données """
        date_now = timezone.now()

        test_user1 = User.objects.create_user(
            username="testuser1", password="testtest"
        )
        test_user2 = User.objects.create_user(
            username="testuser2", password="testtest"
        )

        test_user1.save()
        test_user2.save()

        test_etude1 = RefEtudes.objects.create(
            nom="test_etude1", date_ouverture=date_now
        )
        test_etude2 = RefEtudes.objects.create(
            nom="test_etude2", date_ouverture=date_now
        )

        test_etude1.save()
        test_etude2.save()

        etat_1 = RefEtatEtape.objects.create(nom="test")
        etat_1.save()

        jonction_etude1 = JonctionUtilisateurEtude.objects.create(
            user=test_user1,
            etude=test_etude2,
            date_autorisation=date_now,
        )
        jonction_etude1.save()
        jonction_etude2 = JonctionUtilisateurEtude.objects.create(
            user=test_user2,
            etude=test_etude1,
            date_autorisation=date_now,
        )
        jonction_etude2.save()

        etape_etude = RefEtapeEtude.objects.create(
            nom="Etape_test1", etude=test_etude1
        )
        etape_etude.save()
        etape_etude = RefEtapeEtude.objects.create(
            nom="Etape_test2", etude=test_etude2
        )
        etape_etude.save()

        test_centre = RefInfocentre.objects.create(
            nom="Centre_test1", numero="1258", date_ajout=date_now
        )
        test_centre.save()
        test_centre = RefInfocentre.objects.create(
            nom="Centre_test2", numero="12587", date_ajout=date_now
        )
        test_centre.save()

        doc_1 = SuiviDocument.objects.create(
            user=test_user1,
            etude=test_etude2,
            titre="Test_doc",
            description="Desc_Test_Doc",
            date=date_now,
            fichiers="",
            background="bg-nw-protocole.jpg",
        )
        doc_1.save()

        test_typeaction = RefTypeAction.objects.create(
            id=1, nom="Action_1"
        )
        test_typeaction.save()
        test_typeaction = RefTypeAction.objects.create(
            id=2, nom="Action_2"
        )
        test_typeaction.save()
        test_typeaction = RefTypeAction.objects.create(
            id=3, nom="Action_3"
        )
        test_typeaction.save()
        test_typeaction = RefTypeAction.objects.create(
            id=4, nom="Action_4"
        )
        test_typeaction.save()
        test_typeaction = RefTypeAction.objects.create(
            id=5, nom="Action_5"
        )
        test_typeaction.save()
        test_typeaction = RefTypeAction.objects.create(
            id=6, nom="Action_6"
        )
        test_typeaction.save()
        test_typeaction = RefTypeAction.objects.create(
            id=7, nom="Action_7"
        )
        test_typeaction.save()

    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------
    # TEST DOCUMENTAIRE MODULE
    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------

    def test_gestion_doc(self):
        """Test le module gestion documentaire"""
        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")
        id_user = User.objects.all()
        id_etude = RefEtudes.objects.all()
        files = settings.BASE_DIR + "\\documents\\test_img.png"
        myfile = open(files, "rb")
        val_dict = {
            "user_current": id_user[0],
            "etudes": id_etude[0].id,
            "titre": "Test_doc_ajout",
            "description": "Desc_Test_Doc_ajout",
            "type": 1,
            "document": myfile,
        }
        post_document = self.client.post(
            reverse("gestion"), data=val_dict
        )
        self.assertEqual(post_document.status_code, 200)
        result = post_document.context["resultat"]
        for item in result:
            self.assertIn(item.titre, ["Test_doc_ajout", "Test_doc"])

    def test_doc_edit(self):
        """Test le module d'édition documentaire"""
        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")
        id_user = User.objects.all()
        id_etude = RefEtudes.objects.all()
        files = settings.BASE_DIR + "\\documents\\test_img.png"
        myfile = open(files, "rb")
        val_dict = {
            "user_current": id_user[0],
            "etudes": id_etude[0].id,
            "titre": "Test_doc_edition",
            "description": "Desc_Test_Doc_edition",
            "type": 1,
            "document": myfile,
        }
        post_document = self.client.post(
            reverse("gestion"), data=val_dict
        )
        result = post_document.context["resultat"]
        for item in result:
            if item.titre == "Test_doc_edition":
                id_item = item.id
        edit_document = self.client.post(
            reverse("doc_edit", args=(id_item,)),
            {
                "etudes": id_etude[0].id,
                "titre": "Test_doc_EDITER",
                "description": "Desc_Test_EDITER",
                "type": 1,
            },
        )
        self.assertEqual(edit_document.status_code, 302)
        get_document = self.client.get(reverse("gestion"))
        self.assertEqual(post_document.status_code, 200)
        result = get_document.context["resultat"]
        for item in result:
            self.assertIn(item.titre, ["Test_doc_EDITER", "Test_doc"])

    def test_doc_deleted(self):
        """Test le module de suppression documentaire"""
        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")
        id_user = User.objects.all()
        id_etude = RefEtudes.objects.all()
        files = settings.BASE_DIR + "\\documents\\test_img.png"
        myfile = open(files, "rb")
        val_dict = {
            "user_current": id_user[0],
            "etudes": id_etude[0].id,
            "titre": "Test_doc_deleted",
            "description": "Desc_Test_Doc_deleted",
            "type": 1,
            "document": myfile,
        }
        post_document = self.client.post(
            reverse("gestion"), data=val_dict
        )
        result = post_document.context["resultat"]
        for item in result:
            if item.titre == "Test_doc_deleted":
                id_item = item.id
        edit_document = self.client.post(
            reverse("doc_deleted", args=(id_item,))
        )
        self.assertEqual(edit_document.status_code, 200)
        get_document = self.client.get(reverse("gestion"))
        self.assertEqual(post_document.status_code, 200)
        result = get_document.context["resultat"]
        for item in result:
            self.assertIn(item.titre, ["Test_doc"])
