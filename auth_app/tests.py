from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from datetime import date, time, datetime
from django.utils import timezone

import json


class TestApp(TestCase):
	""" Mise en place des tests """

	def setUp(self):
			""" Mise en place des bases de données """
			date_now = timezone.now()

			test_user1 = User.objects.create_user(
				username="testuser1", password='testtest')
			test_user2 = User.objects.create_user(
				username="testuser2", password='testtest')

			test_user1.save()
			test_user2.save()

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# TEST Login & Logout
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

	def test_login(self):
		''' Test le module login
		'''
		self.client.login(username="testuser1", password='testtest')
		response = self.client.get(reverse('login'))
		self.assertEqual(str(response.context['user']), 'testuser1')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'auth.html')

	def test_logout(self):
		''' Test le module logout
		'''
		self.client.login(username="testuser1", password='testtest')
		response = self.client.get(reverse('login'))
		self.assertEqual(str(response.context['user']), 'testuser1')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'auth.html')
		logout = self.client.get(reverse('logout'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'auth.html')

