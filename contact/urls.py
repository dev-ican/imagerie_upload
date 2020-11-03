# -*-coding:Utf-8 -*

"""Chemin de l'application contact"""

from django.urls import path, re_path

from . import views

urlpatterns = [
	path('', views.gestion_contact, name='contact_gestion'),
	re_path(r'^new/',views.new_contact, name='new_contact'),
	re_path(r'^edit/([0-9]+)/',views.contact_edit, name='contact_edit'),
	re_path(r'^delete/([0-9]+)/',views.contact_deleted, name='contact_deleted'),
]