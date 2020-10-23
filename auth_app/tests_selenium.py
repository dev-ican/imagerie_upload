from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class AccountTestCase(LiveServerTestCase):
    def setUp(self):

        test_user1 = User.objects.create_user(
            username="testuser1", password="testtest"
        )
        test_user2 = User.objects.create_user(
            username="testuser2", password="testtest"
        )
        test_user1.save()
        test_user2.save()

        self.selenium = webdriver.Firefox(
            executable_path="webdriver\\geckodriver.exe"
        )
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def test_auth_log_InOut(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get("http://127.0.0.1:8000/auth/auth_in/")
        # find the form element
        username = selenium.find_element_by_name("log_id")
        password = selenium.find_element_by_name("pwd")
        submit = selenium.find_element_by_name("login")
        # Fill the form with data
        username.send_keys("User_1")
        selenium.implicitly_wait(5)
        password.click()
        password.send_keys("testtest12345")
        # submitting the form
        submit.send_keys(Keys.RETURN)
        selenium.implicitly_wait(10)
        name_index = "Bienvenue User_1 !"
        # check the returned result
        self.assertEqual(
            selenium.find_element_by_css_selector("h1#info_log")
            .get_attribute("innerHTML")
            .splitlines()[0],
            name_index,
        )
        selenium.get("http://127.0.0.1:8000/auth/logout/")
        selenium.implicitly_wait(10)
        name_index = "Vous êtes maintenant déconnecté"
        # check the returned result
        self.assertEqual(
            selenium.find_element_by_css_selector("p.text-warning")
            .get_attribute("innerHTML")
            .splitlines()[0],
            name_index,
        )
