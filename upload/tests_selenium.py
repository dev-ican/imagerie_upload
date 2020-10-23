from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class AccountTestCase(LiveServerTestCase):
    def setUp(self):

        self.selenium = webdriver.Firefox(
            executable_path="webdriver\\geckodriver.exe"
        )
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def test_page_upload(self):
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
        menu_form = selenium.find_element_by_name("form")
        menu_form.click()
        selenium.implicitly_wait(10)
        name_index = "Formulaire d'upload"
        self.assertEqual(
            selenium.find_element_by_name("titre_form")
            .get_attribute("innerHTML")
            .splitlines()[0],
            name_index,
        )

        nip = selenium.find_element_by_name("nip")
        date = selenium.find_element_by_name("date_irm")

        nip.send_keys("test_selenium")
        select = Select(selenium.find_element_by_id("id_etudes"))
        all_options = [
            o.get_attribute("value") for o in select.options
        ]
        for x in all_options:
            if x == 24:
                select.select_by_value(x)
        date.send_keys("2020-01-01")
