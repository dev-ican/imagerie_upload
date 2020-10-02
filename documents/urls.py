# -*-coding:Utf-8 -*

"""Chemin de l'application principal"""

from django.urls import path, re_path

from . import views

urlpatterns = [
	path('', views.gestiondoc, name='gestion'),
	re_path(r'^downOnce/([0-9]+)/',views.downOnce, name='donwnload_once'),
	re_path(r'^edit/([0-9]+)/',views.docEdit, name='doc_edit'),
	re_path(r'^deleted/([0-9]+)/',views.docDeleted, name='doc_deleted'),
]