from django.test import TestCase
from django.urls import reverse

from admin_page.forms import FormsEtude, FormsEtape, FormsAutorisation, FormsUser, FormsUserEdit, FormCentre
from .models import RefEtudes, JonctionUtilisateurEtude, RefEtapeEtude, RefInfocentre, JonctionEtapeSuivi, SuiviUpload

from django.contrib.auth.models import User

# Create your tests here.

class TestApp(TestCase):
	""" Mise en place des tests """

	def setUp(self):
			""" Mise en place des bases de données """
			test_user1 = User.objects.create_user(
				username="testuser1", password='testtest')
			test_user2 = User.objects.create_user(
				username="testuser2", password='testtest')

			test_user1.save()
			test_user2.save()

			test_etude1 = RefEtudes.objects.create(
				nom="test_etude1", date_ouverture='2020-02-02')
			test_etude2 = RefEtudes.objects.create(
				nom="test_etude1", date_ouverture='2020-02-02')

			test_etude1.save()
			test_etude2.save()

			jonction_etude1 = JonctionUtilisateurEtude.objects.create(user=test_user1, etude=test_etude2, date_autorisation='2020-02-02')

			jonction_etude1.save()

	def test_admin_etude(self):
		''' Test le module adminetude
		allows to test the favorites '''
		self.client.login(username="testuser1", password='testtest')
		response = self.client.get(reverse('login'))

		self.assertEqual(str(response.context['user']), 'testuser1')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'log_in.html')

		check_etude = self.client.get('etudes/')

		self.assertTemplateUsed(check_etude, 'admin_etude.html')

		var_etude = check_etude.context['resultat']

		for item in var_etude:
			self.assertIn(item.nom, ['test_etude1', 'test_etude2'])

		post_etude = self.client.post('etudes/', {'nom':'test_case_etude'})

		self.assertEqual(post_etude.status_code, 302)
		self.assertIn(post_etude, ['test_case_etude'])

	def test_etude_edit(self):
		''' Test le module adminetude
		allows to test the favorites '''
		self.client.login(username="testuser1", password='testtest')
		response = self.client.get(reverse('login'))

		self.assertEqual(str(response.context['user']), 'testuser1')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'log_in.html')

		check_etude = self.client.get('etudes/edit/1')

		self.assertTemplateUsed(check_etude, 'admin_etude_edit.html')

		post_edit_etude = self.client.post('etudes/edit/1', {'nom':'test_edit'})

		self.assertEqual(post_edit_etude.status_code, 302)
		self.assertIn(post_edit_etude, ['test_edit'])

	def test_etude_del(self):
		''' Test le module adminetude
		allows to test the favorites '''
		self.client.login(username="testuser1", password='testtest')
		response = self.client.get(reverse('login'))

		self.assertEqual(str(response.context['user']), 'testuser1')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'log_in.html')

		post_etude = self.client.post('etudes/', {'nom':'test_etude_del'})
		select_del = RefEtudes.objects.all()

		for item in select_del :
			if item.nom == "test_etude_del":
				id_select = item.id
				break

		nbr_etude = len(select_del)

		post_edit_etude = self.client.post('etudes/delete/' + id_select)

		select_del = RefEtudes.objects.all()

		nbr_etude_del = len(select_del)
		self.assertTemplateUsed(check_etude, 'admin_etude.html')

		self.assertNotEqual(nbr_etude, nbr_etude_del)


