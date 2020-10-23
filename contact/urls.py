# -*-coding:Utf-8 -*

"""Chemin de l'application principal"""

from django.urls import path, re_path

from . import views

urlpatterns = [
	path('', views.gestioncontact, name='contact_gestion'),
	re_path(r'^new/',views.newContact, name='new_contact'),
	re_path(r'^edit/([0-9]+)/',views.contactEdit, name='contact_edit'),
	re_path(r'^delete/([0-9]+)/',views.contactDeleted, name='contact_deleted'),
]