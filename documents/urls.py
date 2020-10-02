# -*-coding:Utf-8 -*

"""Chemin de l'application principal"""

from django.urls import path, re_path

from . import views

urlpatterns = [
	path('', views.gestiondoc, name='gestion'),
	re_path(r'^downOnce/([0-9]+)/',views.downOnce, name='donwnload_once'),
]