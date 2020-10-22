from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from .forms import UploadForm
from .models import RefEtudes, JonctionUtilisateurEtude, SuiviUpload, RefControleQualite, JonctionEtapeSuivi, DossierUpload, RefEtatEtape, RefEtapeEtude, SuiviDocument, RefInfocentre, RefControleQualite, log, RefTypeAction

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

			test_etude1 = RefEtudes.objects.create(
				nom="test_etude1", date_ouverture=date_now)
			test_etude2 = RefEtudes.objects.create(
				nom="test_etude2", date_ouverture=date_now)
			test_etude1.save()
			test_etude2.save()

			etat_1 = RefEtatEtape.objects.create(id=1, nom="test")
			etat_1.save()

			jonction_etude1 = JonctionUtilisateurEtude.objects.create(user=test_user1, etude=test_etude2, date_autorisation=date_now)
			jonction_etude1.save()
			jonction_etude2 = JonctionUtilisateurEtude.objects.create(user=test_user2, etude=test_etude1, date_autorisation=date_now)
			jonction_etude2.save()

			etape_etude = RefEtapeEtude.objects.create(nom="Etape_test1", etude=test_etude1)
			etape_etude.save()
			etape_etude = RefEtapeEtude.objects.create(nom="Etape_test2", etude=test_etude2)
			etape_etude.save()

			test_centre = RefInfocentre.objects.create(nom="Centre_test1", numero="1258", date_ajout=date_now)
			test_centre.save()
			test_centre = RefInfocentre.objects.create(nom="Centre_test2", numero="12587", date_ajout=date_now)
			test_centre.save()

			qc_insert = RefControleQualite.objects.create(nom="QC_test")
			qc_insert.save()

			create_dossier = DossierUpload.objects.create(user=test_user1, controle_qualite=qc_insert, date=date_now)
			create_dossier.save()

			doc_1 = SuiviDocument.objects.create(user=test_user1, etude=test_etude2, titre="Test_doc", description="Desc_Test_Doc", date=date_now, fichiers='', background='bg-nw-protocole.jpg')
			doc_1.save()

			test_typeaction = RefTypeAction.objects.create(id=1, nom="Action_1")
			test_typeaction.save()
			test_typeaction = RefTypeAction.objects.create(id=2, nom="Action_2")
			test_typeaction.save()
			test_typeaction = RefTypeAction.objects.create(id=3, nom="Action_3")
			test_typeaction.save()
			test_typeaction = RefTypeAction.objects.create(id=4, nom="Action_4")
			test_typeaction.save()
			test_typeaction = RefTypeAction.objects.create(id=5, nom="Action_5")
			test_typeaction.save()
			test_typeaction = RefTypeAction.objects.create(id=6, nom="Action_6")
			test_typeaction.save()
			test_typeaction = RefTypeAction.objects.create(id=7, nom="Action_7")
			test_typeaction.save()

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
# TEST FORMULAIRE MODULE
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

	def test_upload(self):
		''' Test le module formulaire d'upload
		'''
		date_now = timezone.now()
		self.client.login(username="testuser1", password='testtest')
		response = self.client.get(reverse('login'))
		self.assertEqual(str(response.context['user']), 'testuser1')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'auth.html')

		get_form = self.client.get(reverse('formulaire'))
		self.assertEqual(get_form.status_code, 200)
		self.assertTemplateUsed(get_form, 'form_upload.html')

		id_user = User.objects.all()
		id_etude = JonctionUtilisateurEtude.objects.all()
		id_etape = RefEtatEtape.objects.get(id__exact=1)
		val_dict = {'user_current': id_user[0], 'etudes':id_etude[0].id, 'nip':'Test_upload', 'date_irm':date_now, 'id_etape':id_etape}
		post_form = self.client.post(reverse('formulaire'),data=val_dict)
		self.assertEqual(post_form.status_code, 302)
		self.assertTemplateUsed(get_form, 'form_upload.html')


