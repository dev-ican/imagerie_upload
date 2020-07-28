# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Protocoles(models.Model):
    nom = models.CharField(max_length=5000)
    date_ouverture = models.DateTimeField("Date d'ouverture")

    def __str__(self):
        return self.nom

class UtilisateurProtocole(models.Model):
    '''Création du modèle de base de donnée pour les protocoles'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    protocole = models.ForeignKey('Protocoles', on_delete=models.CASCADE)
    date_ajout = models.DateField(auto_now_add=True)