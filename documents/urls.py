# -*-coding:Utf-8 -*

"""Chemin de l'application documents"""

from django.urls import path, re_path

from . import views

urlpatterns = [
	path('', views.gestion_documentaire, name='gestion'),
	re_path(r'^downOnce/([0-9]+)/',views.down_once, name='donwnload_once'),
	re_path(r'^edit/([0-9]+)/',views.doc_edit, name='doc_edit'),
	re_path(r'^deleted/([0-9]+)/',views.doc_deleted, name='doc_deleted'),
]
