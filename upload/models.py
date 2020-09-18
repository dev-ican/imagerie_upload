# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

def user_directory_path(instance, filename):
	# faire en sorte de ramener l'enregistrement MEDIA_ROOT/<centre>/
	print(instance.fichiers)
	id_centre = RefInfocentre.objects.get(user__exact=instance.user.id)
	return '{0}/{1}/{2}/{3}'.format(instance.etude.etude.nom, id_centre, instance.id_patient, filename)


class SuiviUpload(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	etude = models.ForeignKey("JonctionUtilisateurEtude", on_delete=models.CASCADE)
	id_patient = models.CharField(max_length=5000)
	date_upload = models.DateTimeField("Date d'envois")
	date_examen = models.DateTimeField("Date examen")
	dossier = models.ForeignKey("DossierUpload", on_delete=models.CASCADE, blank=True, null=True)
	fichiers = models.FileField(upload_to=user_directory_path, null=True)


class JonctionUtilisateurEtude(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	etude = models.ForeignKey('RefEtudes', on_delete=models.CASCADE)
	date_autorisation = models.DateTimeField("Date d'autorisation")

class RefControleQualite(models.Model):
	'''Création du modèle de base de donnée pour les protocoles'''
	nom = models.CharField(max_length=5000)

	def __str__(self):
		return self.nom

class RefEtudes(models.Model):
	nom = models.CharField(max_length=5000)
	date_ouverture = models.DateTimeField("Date d'ouverture")

	def __str__(self):
		return self.nom

class RefInfocentre(models.Model):
	nom = models.CharField(max_length=5000)
	numero = models.IntegerField(blank=True)
	date_ajout = models.DateTimeField("Date d'ajout")
	user = models.ManyToManyField(User)

	def __str__(self):
		return self.nom

class RefEtapeEtude(models.Model):
	nom = models.CharField(max_length=5000)
	etude = models.ForeignKey("RefEtudes", on_delete=models.CASCADE)

	def __str__(self):
		return self.nom

class RefEtatEtape(models.Model):
	nom = models.CharField(max_length=5000)

	def __str__(self):
		return self.nom

class JonctionEtapeSuivi(models.Model):
	upload = models.ForeignKey("DossierUpload", on_delete=models.CASCADE, blank=True)
	etape = models.ForeignKey("RefEtapeEtude", on_delete=models.CASCADE)
	etat = models.ForeignKey("RefEtatEtape", on_delete=models.CASCADE)
	date = models.DateTimeField("Date de l'étape", blank=True, null=True)

class DossierUpload(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	controle_qualite = models.ForeignKey("RefControleQualite", on_delete=models.CASCADE, null=True)
	date = models.DateTimeField("Date de création")
