from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from upload.models import RefTypeAction


class TestApp(TestCase):
    """ Mise en place des tests """
    def setUp(self):
        """ Mise en place des bases de données """

        test_user1 = User.objects.create_user(
            username="testuser1", password="testtest"
        )
        test_user2 = User.objects.create_user(
            username="testuser2", password="testtest"
        )

        test_user1.save()
        test_user2.save()

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
    # TEST Login & Logout
    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------

    def test_login(self):
        """Test le module login"""
        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")

    def test_logout(self):
        """Test le module logout"""
        self.client.login(username="testuser1", password="testtest")
        response = self.client.get(reverse("login"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")
        self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth.html")
