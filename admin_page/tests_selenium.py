# -*- coding: utf-8 -*-

"""Permet de tester les pages de la partie admin de l'application."""

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class AccountTestCase(LiveServerTestCase):
    def setUp(self):

        self.selenium = webdriver.Firefox(
            executable_path="webdriver\\geckodriver.exe"
        )
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def test_page_graphique(self):
        """Affiche la page résumant en graphique l'utilisation des fichiers
        chargés."""
        selenium = self.selenium
        selenium.get("http://127.0.0.1:8000/auth/auth_in/")
        username = selenium.find_element_by_name("log_id")
        password = selenium.find_element_by_name("pwd")
        submit = selenium.find_element_by_name("login")
        username.send_keys("User_1")
        selenium.implicitly_wait(5)
        password.click()
        password.send_keys("testtest12345")
        submit.send_keys(Keys.RETURN)
        selenium.implicitly_wait(10)
        menu_form = selenium.find_element_by_name(
            "administration"
        )
        menu_form.click()
        selenium.implicitly_wait(10)
        name_index = (
            "Graphique d'utilisation et de suivi des étapes"
        )
        self.assertEqual(
            selenium.find_element_by_name("titre_graphique")
            .get_attribute("innerHTML")
            .splitlines()[0],
            name_index,
        )

    def test_page_etude(self):
        """Affiche la page des études."""
        selenium = self.selenium
        selenium.get("http://127.0.0.1:8000/auth/auth_in/")
        username = selenium.find_element_by_name("log_id")
        password = selenium.find_element_by_name("pwd")
        submit = selenium.find_element_by_name("login")
        username.send_keys("User_1")
        selenium.implicitly_wait(5)
        password.click()
        password.send_keys("testtest12345")
        submit.send_keys(Keys.RETURN)
        selenium.implicitly_wait(10)
        menu_form = selenium.find_element_by_name(
            "administration"
        )
        menu_form.click()
        selenium.implicitly_wait(10)
        menu_form = selenium.find_element_by_id("menuSuiviEtude")
        menu_form.click()
        selenium.implicitly_wait(10)
        name_index = "Suivi des études"
        self.assertEqual(
            selenium.find_element_by_css_selector(
                "h3.titre_etude"
            )
            .get_attribute("innerHTML")
            .splitlines()[0],
            name_index,
        )

    def test_page_admin_etude(self):
        """Affiche la page d'ajout/edition/suppression d'études."""
        selenium = self.selenium
        selenium.get("http://127.0.0.1:8000/auth/auth_in/")
        username = selenium.find_element_by_name("log_id")
        password = selenium.find_element_by_name("pwd")
        submit = selenium.find_element_by_name("login")
        username.send_keys("User_1")
        selenium.implicitly_wait(5)
        password.click()
        password.send_keys("testtest12345")
        submit.send_keys(Keys.RETURN)
        selenium.implicitly_wait(10)
        menu_form = selenium.find_element_by_name(
            "administration"
        )
        menu_form.click()
        selenium.implicitly_wait(10)
        menu_form = selenium.find_element_by_id("menuEtudes")
        menu_form.click()
        selenium.implicitly_wait(10)
        name_index = "Vos études actuellement enregistrées"
        self.assertEqual(
            selenium.find_element_by_name("titre_TabEtude")
            .get_attribute("innerHTML")
            .splitlines()[0],
            name_index,
        )

    def test_page_admin_etape(self):
        """Affiche la page d'ajout/edition/suppression d'étapes."""
        selenium = self.selenium
        selenium.get("http://127.0.0.1:8000/auth/auth_in/")
        username = selenium.find_element_by_name("log_id")
        password = selenium.find_element_by_name("pwd")
        submit = selenium.find_element_by_name("login")
        username.send_keys("User_1")
        selenium.implicitly_wait(5)
        password.click()
        password.send_keys("testtest12345")
        submit.send_keys(Keys.RETURN)
        selenium.implicitly_wait(10)
        menu_form = selenium.find_element_by_name(
            "administration"
        )
        menu_form.click()
        selenium.implicitly_wait(10)
        menu_form = selenium.find_element_by_id("menuEtapes")
        menu_form.click()
        selenium.implicitly_wait(10)
        name_index = "Indiquer les étapes des etudes"
        self.assertEqual(
            selenium.find_element_by_name("titre_TabEtape")
            .get_attribute("innerHTML")
            .splitlines()[0],
            name_index,
        )

    def test_page_admin_centre(self):
        """Affiche la page d'ajout/edition/suppression de centre."""
        selenium = self.selenium
        selenium.get("http://127.0.0.1:8000/auth/auth_in/")
        username = selenium.find_element_by_name("log_id")
        password = selenium.find_element_by_name("pwd")
        submit = selenium.find_element_by_name("login")
        username.send_keys("User_1")
        selenium.implicitly_wait(5)
        password.click()
        password.send_keys("testtest12345")
        submit.send_keys(Keys.RETURN)
        selenium.implicitly_wait(10)
        menu_form = selenium.find_element_by_name(
            "administration"
        )
        menu_form.click()
        selenium.implicitly_wait(10)
        menu_form = selenium.find_element_by_id("menuCentres")
        menu_form.click()
        selenium.implicitly_wait(10)
        name_index = "Les centres actuellement enregistrés"
        self.assertEqual(
            selenium.find_element_by_name("titre_TabCentre")
            .get_attribute("innerHTML")
            .splitlines()[0],
            name_index,
        )

    def test_page_admin_auth(self):
        """Affiche la page de paramétrage des droits."""
        selenium = self.selenium
        selenium.get("http://127.0.0.1:8000/auth/auth_in/")
        username = selenium.find_element_by_name("log_id")
        password = selenium.find_element_by_name("pwd")
        submit = selenium.find_element_by_name("login")
        username.send_keys("User_1")
        selenium.implicitly_wait(5)
        password.click()
        password.send_keys("testtest12345")
        submit.send_keys(Keys.RETURN)
        selenium.implicitly_wait(10)
        menu_form = selenium.find_element_by_name(
            "administration"
        )
        menu_form.click()
        selenium.implicitly_wait(10)
        menu_form = selenium.find_element_by_id("menuUserAuth")
        menu_form.click()
        selenium.implicitly_wait(10)
        name_index = "Vos utilisateurs actuellement enregistrés"
        self.assertEqual(
            selenium.find_element_by_name("titre_AutUser")
            .get_attribute("innerHTML")
            .splitlines()[0],
            name_index,
        )

    def test_page_admin_user(self):
        """Affiche la page d'ajout/edition/suppression d'utilisateur."""
        selenium = self.selenium
        selenium.get("http://127.0.0.1:8000/auth/auth_in/")
        username = selenium.find_element_by_name("log_id")
        password = selenium.find_element_by_name("pwd")
        submit = selenium.find_element_by_name("login")
        username.send_keys("User_1")
        selenium.implicitly_wait(5)
        password.click()
        password.send_keys("testtest12345")
        submit.send_keys(Keys.RETURN)
        selenium.implicitly_wait(10)
        menu_form = selenium.find_element_by_name(
            "administration"
        )
        menu_form.click()
        selenium.implicitly_wait(10)
        menu_form = selenium.find_element_by_id("menuUser")
        menu_form.click()
        selenium.implicitly_wait(10)
        name_index = "Les utilisateurs actuellement enregistrés"
        self.assertEqual(
            selenium.find_element_by_name("titre_user")
            .get_attribute("innerHTML")
            .splitlines()[0],
            name_index,
        )

    def test_page_admin_doc(self):
        """Affiche la page d'ajout/edition/suppression des documents."""
        selenium = self.selenium
        selenium.get("http://127.0.0.1:8000/auth/auth_in/")
        username = selenium.find_element_by_name("log_id")
        password = selenium.find_element_by_name("pwd")
        submit = selenium.find_element_by_name("login")
        username.send_keys("User_1")
        selenium.implicitly_wait(5)
        password.click()
        password.send_keys("testtest12345")
        submit.send_keys(Keys.RETURN)
        selenium.implicitly_wait(10)
        menu_form = selenium.find_element_by_name(
            "administration"
        )
        menu_form.click()
        selenium.implicitly_wait(10)
        menu_form = selenium.find_element_by_id("menuDoc")
        menu_form.click()
        selenium.implicitly_wait(10)
        name_index = "Les documents enregistrés"
        self.assertEqual(
            selenium.find_element_by_name("titre_document")
            .get_attribute("innerHTML")
            .splitlines()[0],
            name_index,
        )
