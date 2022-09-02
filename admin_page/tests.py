import json

from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from upload.models import (
    DossierUpload,
    JonctionUtilisateurEtude,
    RefControleQualite,
    RefEtapeEtude,
    RefEtatEtape,
    RefEtudes,
    RefInfoCentre,
    RefTypeAction,
    SuiviUpload,
)


class TestApp(TestCase):
    """Mise en place des tests."""

    def setUp(self):
        """Mise en place des bases de données."""
        date_now = timezone.now()

        groupe_collaborateur = Group.objects.create(name='Utilisateurs')

        test_user1 = User.objects.create_user(username="testuser1", password="testtest")
        test_user2 = User.objects.create_user(username="testuser2", password="testtest")
        test_user3 = User.objects.create_user(username="testuser3", password="testtest")
    
        groupe_collaborateur.user_set.add(test_user1, test_user2, test_user3)

        test_etude1 = RefEtudes.objects.create(nom="test_etude1", date_ouverture=date_now)
        test_etude2 = RefEtudes.objects.create(nom="test_etude2", date_ouverture=date_now)

        etat_01 = RefEtatEtape.objects.create(nom="Nouveau")
        etat_02 = RefEtatEtape.objects.create(nom="En cours")
        etat_03 = RefEtatEtape.objects.create(nom="Erreur")
        etat_04 = RefEtatEtape.objects.create(nom="Demandes d'informations")
        etat_05 = RefEtatEtape.objects.create(nom="Terminé")

        jonction_etude1 = (JonctionUtilisateurEtude.objects.create(user=test_user1,
                                                                   etude=test_etude2,
                                                                   date_autorisation=date_now,
                                                                   ))
        jonction_etude2 = (JonctionUtilisateurEtude.objects.create(user=test_user2,
                                                                   etude=test_etude1,
                                                                   date_autorisation=date_now,
                                                                   ))
        jonction_etude3 = (JonctionUtilisateurEtude.objects.create(user=test_user3,
                                                                   etude=test_etude1,
                                                                   date_autorisation=date_now,
                                                                   ))

        etape_etude = RefEtapeEtude.objects.create(nom="Etape_test1")
        etape_etude.etude.add(test_etude1)
        etape_etude.save()

        etape_etude = RefEtapeEtude.objects.create(nom="Etape_test2")
        etape_etude.etude.add(test_etude2)
        etape_etude.save()

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

        RefTypeAction.objects.create(id=1, nom="Action_1")
        RefTypeAction.objects.create(id=2, nom="Action_2")
        RefTypeAction.objects.create(id=3, nom="Action_3")
        RefTypeAction.objects.create(id=4, nom="Action_4")
        RefTypeAction.objects.create(id=5, nom="Action_5")
        RefTypeAction.objects.create(id=6, nom="Action_6")
        RefTypeAction.objects.create(id=7, nom="Action_7")

        test_cq = RefControleQualite.objects.create(id=1, nom="QC_1")

        test_dossier = DossierUpload.objects.create(id=1,
                                                    user=test_user1,
                                                    controle_qualite=test_cq,
                                                    date="2020-10-22",
                                                   )

        test_suivi = SuiviUpload.objects.create(id=1,
                                                user=test_user1,
                                                etude=jonction_etude1,
                                                id_patient="Suivi_test",
                                                date_upload="2020-10-22",
                                                date_examen="2020-10-22",
                                                dossier=test_dossier,
                                                fichiers="",
                                                )

    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------
    # TEST ETUDE MODULE
    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------


    def test_admin_etude(self):
        """Test le module admin etude."""

        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")

        check_etude = self.client.get(reverse("admin_etude"))
        self.assertTemplateUsed(check_etude, "admin_etude.html")

        var_etude = check_etude.context["resultat"]
        for item in var_etude:
            self.assertIn(item.nom, ["test_etude1", "test_etude2"])

        post_etude = self.client.post(reverse("admin_etude"), {"nom": "test_case_etude"})
        self.assertEqual(post_etude.status_code, 200)

        reponse = False
        for item in post_etude.context["resultat"]:
            if item.nom == "test_case_etude":
                reponse = True
        self.assertTrue(reponse)


    def test_etude_edit(self):
        """Test le module admin etude edition."""
        
        date_now = timezone.now()
        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")

        val_dict = {"nom": "test_etude1"}

        post_etude = self.client.post(reverse("admin_etude"), data=val_dict)
        self.assertEqual(post_etude.status_code, 200)

        etudes = RefEtudes.objects.all()
        for etude in etudes:
            if etude.nom == "test_etude1":
                etude_id = etude.id
                break
        
        post_edit_etude = self.client.post(reverse("etude_edit", args=(etude_id,)), {"nom": "test_edit",
                                                                                     "date": date_now
                                                                                     })
        self.assertEqual(post_edit_etude.status_code, 302)
        
        projet_id = RefEtudes.objects.all()
        reponse = False

        for item_edit in projet_id:
            if item_edit.nom == "test_edit":
                reponse = True
        self.assertTrue(reponse)


    def test_etude_del(self):
        """Test le module admin etude suppr."""

        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")

        val_dict = {"nom": "test_etude_del"}
        post_etude = self.client.post(reverse("admin_etude"), data=val_dict)
        self.assertEqual(post_etude.status_code, 200)
        
        select_del = RefEtudes.objects.all()
        for item in select_del:
            if item.nom == "test_etude_del":
                id_select = item.id
                break
        nbr_etude = len(select_del)
        projet_id = id_select
        post_edit_etude = self.client.post(reverse("etude_suppr", args=(projet_id,)))
        select_del = RefEtudes.objects.all()
        nbr_etude_del = len(select_del)
        self.assertTemplateUsed(post_edit_etude, "admin_etude.html")
        self.assertNotEqual(nbr_etude, nbr_etude_del)

    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------
    # TEST ETAPE MODULE
    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------

    def test_admin_etape(self):
        """Test le module admin etape."""

        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")

        check_etude = self.client.get(reverse("admin_etape"))
        self.assertTemplateUsed(check_etude, "admin_etapes.html")
        var_etude = check_etude.context["resultat"]
        for item in var_etude:
            self.assertIn(item.nom, ["Etape_test1", "Etape_test2"])
                
        id_etude = RefEtudes.objects.get(nom__exact="test_etude1")
        post_etape = self.client.post(reverse("admin_etape"), {"nom": "test_case_etape",
                                                               "etudes": id_etude.id
                                                              })
        self.assertEqual(post_etape.status_code, 200)

        reponse = False
        for item in post_etape.context["resultat"]:
            if item.nom == "test_case_etape":
                reponse = True
        self.assertTrue(reponse)


    def test_admin_etape_edit(self):
        """Test le module admin d'édition d'étapes."""
        
        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")
        
        etude = RefEtudes.objects.get(nom__exact="test_etude1")
        val_dict = {"nom": "test_etape_edit",
                    "etudes": etude.id,
                   }
        post_etape = self.client.post(reverse("admin_etape"), data=val_dict)
        self.assertEqual(post_etape.status_code, 200)

        etapes = RefEtapeEtude.objects.all()
        for etape in etapes:
            if etape.nom == "test_etape_edit":
                etape_id = etape.id
                break

        id_etape = RefEtapeEtude.objects.get(id__exact=etape_id)
        check_etape = self.client.get(reverse("etape_edit", args=(etape_id,)))
        self.assertEqual(check_etape.status_code, 200)
        self.assertTemplateUsed(check_etape, "admin_etapes_edit.html")

        var_etape = check_etape.context["resultat"]
        for item in var_etape:
            self.assertIn(item.nom, ["Etape_test1",
                                     "Etape_test2",
                                     "test_etape_edit",
                                    ])

        post_etape = self.client.post(reverse("etape_edit", args=(id_etape.id,)),
                                                            data={"nom": "test_case_etape",
                                                                  "etudes": id_etape.etude,
                                                                  })
        self.assertEqual(post_etape.status_code, 302)

        check = self.client.get(reverse("admin_etape"))
        reponse = False
        for item in check.context["resultat"]:
            if item.nom == "test_case_etape":
                reponse = True
        self.assertTrue(reponse)


    def test_admin_etape_del(self):
        """Test le module admin etape suppr."""
        
        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")

        id_etude = RefEtudes.objects.get(nom__exact="test_etude1")
        val_dict = {"nom": "test_etape_del",
                    "etudes": id_etude.id,
                   }
        post_etape = self.client.post(reverse("admin_etape"), data=val_dict)
        self.assertEqual(post_etape.status_code, 200)
        
        select_del = RefEtapeEtude.objects.all()
        for item in select_del:
            if item.nom == "test_etape_del":
                id_select = item.id
                break
        nbr_etape = len(select_del)
        projet_id = id_select
        post_edit_etape = self.client.post(reverse("etape_suppr", args=(projet_id,)))
        select_del = RefEtudes.objects.all()
        nbr_etape_del = len(select_del)
        self.assertTemplateUsed(post_edit_etape, "admin_etapes.html")
        self.assertNotEqual(nbr_etape, nbr_etape_del)

    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------
    # TEST USER MODULE
    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------


    def test_admin_user(self):
        """Test le module admin user."""

        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")

        check_user = self.client.get(reverse("admin_utilisateur"))
        self.assertTemplateUsed(check_user, "admin_user.html")

        var_user = check_user.context["resultat"]
        for item in var_user:
            self.assertIn(item.username, ["testuser1",
                                          "testuser2",
                                          "testuser3",
                                          "testuser4",
                                         ])
        
        centre = RefInfoCentre.objects.get(nom="Centre_test1")

        dict_user = {"username": "test_user_create",
                     "email": "test_email@gmail.com",
                     "pass_first": "testtest12345",
                     "pass_second": "testtest12345",
                     "centre": centre.id,
                    #  "nom": "",
                    #  "numero": "",
                     "type": 1,
                    }
        post_user = self.client.post(reverse("admin_utilisateur"), data=dict_user)
        self.assertEqual(post_user.status_code, 200)

        reponse = False
        for item in post_user.context["resultat"]:
            if item.username == "test_user_create":
                reponse = True
        self.assertTrue(reponse)


    def test_admin_user_edit(self):

        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")

        centre = RefInfoCentre.objects.get(nom="Centre_test1")

        val_dict = {"username": "test_user_edit",
                    "email": "test_user@gmail.com",
                    "pass_first": "testtest12345",
                    "pass_second": "testtest12345",
                    "centre": centre.id,
                    # "nom": "",
                    # "numero": "",
                    "type": 1,
                   }

        post_user = self.client.post(reverse("admin_utilisateur"), data=val_dict)
        self.assertEqual(post_user.status_code, 200)

        users = User.objects.all()
        for user in users:
            if user.username == "test_user_edit":
                user_id = user.id
                break

        id_user = User.objects.get(id__exact=user_id)
        check_user = self.client.get(reverse("user_edit", args=(user_id,)))
        self.assertEqual(check_user.status_code, 200)
        self.assertTemplateUsed(check_user, "admin_user_edit.html")

        var_etude = check_user.context["resultat"]
        for item in var_etude:
            self.assertIn(item.username, ["testuser1",
                                          "testuser2",
                                          "test_user_edit",
                                          "testuser3",
                                          "testuser4",
                                         ])

        post_user = self.client.post(reverse("user_edit", args=(id_user.id,)), data={"username": "user_edit",
                                                                                     "email": id_user.email,
                                                                                     "pass_first": "",
                                                                                     "pass_second": "",
                                                                                     "type": 1,
                                                                                    })
        self.assertEqual(post_user.status_code, 302)

        check = self.client.get(reverse("admin_utilisateur"))
        reponse = False
        for item in check.context["resultat"]:
            if item.username == "user_edit":
                reponse = True
        self.assertTrue(reponse)


    def test_admin_user_del(self):
        """Test le module admin de suppression d'utilisateur"""
        
        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")

        centre = RefInfoCentre.objects.get(nom="Centre_test1")

        val_dict = {"username": "test_user_del",
                    "email": "test_user@gmail.com",
                    "pass_first": "testtest12345",
                    "pass_second": "testtest12345",
                    "centre": centre.id,
                    # "nom": "",
                    # "numero": "",
                    "type": 1,
                   }
        post_user = self.client.post(reverse("admin_utilisateur"), data=val_dict)
        self.assertEqual(post_user.status_code, 200)

        select_del = User.objects.all()
        for item in select_del:
            if item.username == "test_user_del":
                id_select = item.id
                break
        nbr_etape = len(select_del)
        projet_id = id_select
        post_user = self.client.post(reverse("user_suppr", args=(projet_id,)))
        select_del = User.objects.all()
        nbr_etape_del = len(select_del)
        self.assertTemplateUsed(post_user, "admin_user.html")
        self.assertNotEqual(nbr_etape, nbr_etape_del)


    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------
    # TEST CENTRE MODULE
    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------


    def test_admin_centre(self):
        """Test le module admin centre."""

        date_now = timezone.now()
        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")

        check_user = self.client.get(reverse("admin_centre"))
        self.assertTemplateUsed(check_user, "admin_centre.html")
        var_user = check_user.context["resultat"]
        for item in var_user:
            # self.assertIn(item["nom"], ["Centre_test1", "Centre_test2"])
            self.assertIn(item.nom, ["Centre_test1", "Centre_test2"])
        
        dict_centre = {
                      "nom": "test_centre_create",
                      "numero": "569",
                      "date_ajout": date_now,
                      }
        post_centre = self.client.post(reverse("admin_centre"), data=dict_centre)
        self.assertEqual(post_centre.status_code, 200)

        reponse = False
        for item in post_centre.context["resultat"]:
            # if item["nom"] == "test_centre_create":
            if item.nom == "test_centre_create":
                reponse = True
        self.assertTrue(reponse)


    def test_admin_centre_edit(self):
        """Test le module admin centre edition."""

        date_now = timezone.now()
        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")

        val_dict = {"nom": "test_centre_edit",
                    "numero": "125",
                    # "utilisateurs": 
                    # "date_ajout": date_now,
                   }
        post_user = self.client.post(reverse("admin_centre"), data=val_dict)
        self.assertEqual(post_user.status_code, 200)

        select_del = RefInfoCentre.objects.all()
        for item in select_del:
            if item.nom == "test_centre_edit":
                id_projet = item.id
                break
        id_centre = RefInfoCentre.objects.get(id__exact=id_projet)
        check_user = self.client.get(reverse("centre_edit", args=(id_projet,)))
        self.assertEqual(check_user.status_code, 200)
        self.assertTemplateUsed(check_user, "admin_centre_edit.html")

        var_etude = check_user.context["resultat"]
        for item in var_etude:
            self.assertIn(item.nom, ["Centre_test1",
                                    "Centre_test2",
                                    "test_centre_edit",
                                    ])

        post_centre = self.client.post(reverse("centre_edit", args=(id_centre.id,)), data={"nom": "centre_edit",
                                                                                           "numero": "56987",
                                                                                        #    "date_ajout": date_now,
                                                                                          })
        self.assertEqual(post_centre.status_code, 302)
        
        check = self.client.get(reverse("admin_centre"))
        reponse = False
        for item in check.context["resultat"]:
            # if item["nom"] == "centre_edit":
            if item.nom == "centre_edit":
                reponse = True
        self.assertTrue(reponse)


    def test_admin_centre_del(self):
        """Test le module admin centre suppr."""

        date_now = timezone.now()
        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")

        val_dict = {"nom": "test_centre_del",
                    "numero": "6879",
                    "date_ajout": date_now,
                    }
        post_centre = self.client.post(reverse("admin_centre"), data=val_dict)
        self.assertEqual(post_centre.status_code, 200)

        select_del = RefInfoCentre.objects.all()
        for item in select_del:
            if item.nom == "test_centre_del":
                id_select = item.id
                break
        nbr_etape = len(select_del)
        projet_id = id_select
        post_user = self.client.post(reverse("centre_suppr", args=(projet_id,)))
        select_del = RefInfoCentre.objects.all()
        nbr_etape_del = len(select_del)
        self.assertTemplateUsed(post_user, "admin_centre.html")
        self.assertNotEqual(nbr_etape, nbr_etape_del)


    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------
    # TEST AUTHENTIFICATION MODULE
    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------


    def test_admin_auth(self):
        """Test le module admin autorisation."""

        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")

        check_user = self.client.get(reverse("admin_autorisation"))
        self.assertEqual(check_user.status_code, 200)
        self.assertTemplateUsed(check_user, "admin_autorisation.html")
        
        var_user = check_user.context["resultat"]
        for item in var_user:
            self.assertIn(item.username, ["testuser1",
                                          "testuser2",
                                          "testuser3",
                                          "testuser4",
                                          ])


    def test_admin_auth_edit(self):
        """Test le module admin autorisation edition."""

        self.client.login(username="testuser1",
                          password="testtest"
                          )
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]),"testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")

        centre = RefInfoCentre.objects.get(nom="Centre_test1")
        
        val_dict = {"username": "test_user_Auth",
                    "email": "test_user@gmail.com",
                    "pass_first": "testtest12345",
                    "pass_second": "testtest12345",
                    "centre": centre.id,
                    # "nom": "",
                    # "numero": "",
                    "type": 1,
                    }
        post_user = self.client.post(reverse("admin_utilisateur"), data=val_dict)
        self.assertEqual(post_user.status_code, 200)
        
        select_del = User.objects.all()
        for item in select_del:
            if item.username == "test_user_Auth":
                id_projet = item.id
                break
        check_user = self.client.get(reverse("auth_edit", args=(id_projet,)))
        self.assertEqual(check_user.status_code, 200)
        self.assertTemplateUsed(check_user, "admin_auth_edit.html")

        var_etude = check_user.context["etude"]
        var_centre = check_user.context["centre"]
        for item in var_etude:
            self.assertIn(item.nom, ["test_etude1", "test_etude2"])

        for item in var_centre:
            self.assertIn(item.nom, ["Centre_test1", "Centre_test2"])

        etude_all = RefEtudes.objects.all()
        centre_all = RefInfoCentre.objects.all()
        for item in etude_all:
            dict_etude = item.id
        for item in centre_all:
            dict_centre = item.id
        post_centre = self.client.post(reverse("auth_edit", args=(id_projet,)), data={"centre": dict_centre,
                                                                                      "etude": dict_etude
                                                                                      })
        self.assertEqual(post_centre.status_code, 200)


    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------
    # TEST MODULE STAT
    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------


    def test_stat_page(self):
        """Test le module d'affichage de la page de stat."""

        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")

        check_user = self.client.get(reverse("admin"))
        self.assertEqual(check_user.status_code, 200)
        self.assertTemplateUsed(check_user, "admin_page.html")


    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------
    # TEST AFFICHAGE TABLEAU ETAT ETAPE
    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------


    def test_page_etat(self):
        """Test le module d'affichage pour la page état étapes."""

        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")

        check_user = self.client.get(reverse("admin_upload"))
        self.assertEqual(check_user.status_code, 200)
        self.assertTemplateUsed(check_user, "admin_page_upload.html")


    # def test_page_etat_tris(self):
    #     """Test le module tris pour la page état étapes."""

    #     self.client.login(username="testuser1", password="testtest")
    #     response = self.client.get(reverse("login"))
    #     self.assertEqual(str(response.context["user"]), "testuser1")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "auth.html")

    #     id_etude = RefEtudes.objects.filter(id__gte=0)[:1]
    #     get_tris = self.client.get(reverse("upload_tris", args=(id_etude[0].id,)))
    #     self.assertTemplateUsed(get_tris, "admin_page_upload.html")
    #     self.assertEqual(get_tris.status_code, 200)
    #     self.assertEqual(len(get_tris.context["resultat"]), 0)


    def test_page_etat_mod(self):
        """Test le module modification qui ramène la liste déroulante pour la
        page état étapes."""

        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")

        get_mod = self.client.get(reverse("upload_mod"))
        result = json.loads(get_mod.content)
        self.assertEqual(len(result), 306)
