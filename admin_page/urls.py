# -*-coding:Utf-8 -*

"""Chemin de l'application principal"""

from django.urls import path, re_path

from . import views

urlpatterns = [
	path('', views.adminpage, name='admin'),
	path('etudes/', views.adminetude, name='admin_etude'),
	path('etapes/', views.adminetape, name='admin_etape'),
	re_path(r'^etapes/edit/([0-9]+)/',views.etapeEdit, name='etape_edit'),
]