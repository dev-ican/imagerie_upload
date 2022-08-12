# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from upload.models import Contact, RefTypeAction


class TestApp(TestCase):
    """Mise en place des tests."""

    def setUp(self):
        """Mise en place des bases de données."""
        date_now = timezone.now()

        test_user1 = User.objects.create_user(username="testuser1",
                                              password="testtest"
                                              )
        test_user2 = User.objects.create_user(username="testuser2",
                                              password="testtest"
                                              )

        test_contact1 = Contact.objects.create(nom="Nom_contact1",
                                               prenom="Prenom_contact1",
                                               courriel="test@test.com",
                                               telephone="0147896523",
                                               poste="Test contact",
                                               )
        test_contact2 = Contact.objects.create(nom="Nom_contact2",
                                               prenom="Prenom_contact2",
                                               courriel="test@test.com",
                                               telephone="0147896523",
                                               poste="Test contact_2",
                                               )

        RefTypeAction.objects.create(id=1, nom="Action_1")
        RefTypeAction.objects.create(id=2, nom="Action_2")
        RefTypeAction.objects.create(id=3, nom="Action_3")
        RefTypeAction.objects.create(id=4, nom="Action_4")
        RefTypeAction.objects.create(id=5, nom="Action_5")
        RefTypeAction.objects.create(id=6, nom="Action_6")
        RefTypeAction.objects.create(id=7, nom="Action_7")

    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------
    # TEST DOCUMENTAIRE MODULE
    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------

    def test_gestion_contact(self):
        """Test le module gestion de contact."""

        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")
        id_user = User.objects.all()
        id_contact = Contact.objects.all()

        val_dict = {
            "nom": "Nom_contact1_ajout",
            "prenom": "Prenom_contact1",
            "email": "test@test.com",
            "telephone": "0147896523",
            "poste": "Test contact",
        }

        post_document = self.client.post(reverse("new_contact"), data=val_dict)
        self.assertEqual(post_document.status_code, 302)
        get_document = self.client.get(reverse("contact_gestion"))
        result = get_document.context["resultat"]

        for item in result:
            self.assertIn(item.nom, ["Nom_contact1_ajout",
                                     "Nom_contact1",
                                     "Nom_contact2",
                                     ])


    def test_contact_edit(self):
        """Test le module d'édition documentaire."""

        self.client.login(
            username="testuser1", password="testtest"
        )
        response = self.client.get(reverse("login"))
        self.assertEqual(
            str(response.context["user"]), "testuser1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")
        id_user = User.objects.all()
        id_etude = Contact.objects.all()
        val_dict = {
            "nom": "Nom_contact1_edition",
            "prenom": "Prenom_contact1",
            "email": "test@test.com",
            "telephone": "0147896523",
            "poste": "Test contact",
        }
        post_document = self.client.post(
            reverse("new_contact"), data=val_dict
        )
        get_contact = self.client.get(reverse("contact_gestion"))
        result = get_contact.context["resultat"]
        for item in result:
            if item.nom == "Nom_contact1_edition":
                id_item = item.id
        edit_document = self.client.post(
            reverse("contact_edit", args=(id_item,)),
            {
                "nom": "Nom_contact1_EDITE",
                "prenom": "Prenom_contact1_EDITE",
                "email": "test@edition.com",
                "telephone": "0147896523",
                "poste": "EDITER",
            },
        )
        self.assertEqual(edit_document.status_code, 302)
        get_document = self.client.get(
            reverse("contact_gestion")
        )
        self.assertEqual(post_document.status_code, 302)
        result = get_document.context["resultat"]
        for item in result:
            self.assertIn(
                item.nom,
                [
                    "Nom_contact1_EDITE",
                    "Nom_contact1",
                    "Nom_contact2",
                ],
            )

    def test_contact_deleted(self):
        """Test le module de suppression documentaire."""
        self.client.login(
            username="testuser1", password="testtest"
        )
        response = self.client.get(reverse("login"))
        self.assertEqual(
            str(response.context["user"]), "testuser1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")
        id_user = User.objects.all()
        id_etude = Contact.objects.all()
        val_dict = {
            "nom": "Nom_contact1_del",
            "prenom": "Prenom_contact1",
            "email": "test@test.com",
            "telephone": "0147896523",
            "poste": "Test contact",
        }
        post_document = self.client.post(
            reverse("new_contact"), data=val_dict
        )
        get_contact = self.client.get(reverse("contact_gestion"))
        result = get_contact.context["resultat"]
        for item in result:
            if item.nom == "Nom_contact1_del":
                id_item = item.id
        edit_document = self.client.post(
            reverse("contact_deleted", args=(id_item,))
        )
        self.assertEqual(edit_document.status_code, 200)
        get_document = self.client.get(
            reverse("contact_gestion")
        )
        self.assertEqual(post_document.status_code, 302)
        result = get_document.context["resultat"]
        for item in result:
            self.assertIn(
                item.nom, ["Nom_contact1", "Nom_contact2"]
            )
