from django.test import TestCase
from django.urls import reverse

from .models import Produits, Favoris, categories

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

	        test_etude1 = User.objects.create_user(
	            nom="test_etude1", date_ouverture='2020-02-02')
	        test_etude2 = User.objects.create_user(
	            nom="test_etude1", date_ouverture='2020-02-02')

	        test_etude1.save()
	        test_etude2.save()

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


