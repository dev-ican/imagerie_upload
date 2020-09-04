# -*-coding:Utf-8 -*

"""Chemin de l'application principal"""

from django.urls import path, re_path

from . import views

urlpatterns = [
	path('', views.adminpage, name='admin'),
	path('etudes/', views.adminetude, name='admin_etude'),
	re_path(r'^etudes/edit/([0-9]+)/',views.etudeEdit, name='etude_edit'),
	re_path(r'^etudes/delete/([0-9]+)/',views.etudeDel, name='etude_suppr'),	
	path('etapes/', views.adminetape, name='admin_etape'),
	re_path(r'^etapes/edit/([0-9]+)/',views.etapeEdit, name='etape_edit'),
	re_path(r'^etapes/delete/([0-9]+)/',views.etapeDel, name='etape_suppr'),
	path('viewUser/', views.adminuser, name='admin_utilisateur'),
	re_path(r'^viewUser/edit/([0-9]+)/',views.userEdit, name='user_edit'),
	path('centre/', views.admincentre, name='admin_centre'),
	re_path(r'^centre/edit/([0-9]+)/',views.centreEdit, name='auth_edit'),
	path('userAuth/', views.adminauth, name='admin_autorisation'),
	re_path(r'^userAuth/edit/([0-9]+)/',views.authEdit, name='auth_edit'),
]