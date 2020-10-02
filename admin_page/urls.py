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
	re_path(r'^viewUser/delete/([0-9]+)/',views.userDel, name='user_suppr'),
	path('centre/', views.admincentre, name='admin_centre'),
	re_path(r'^centre/edit/([0-9]+)/',views.centreEdit, name='centre_edit'),
	re_path(r'^centres/delete/([0-9]+)/',views.centreDel, name='centre_suppr'),
	path('userAuth/', views.adminauth, name='admin_autorisation'),
	re_path(r'^userAuth/edit/([0-9]+)/',views.authEdit, name='auth_edit'),
	re_path(r'^userAuth/delete',views.authDel, name='auth_suppr'),
	path('upfiles/', views.adminup, name='admin_upload'),
	re_path(r'^upfiles/tris/([0-9]+)/',views.uploadtris, name='upload_tris'),
	re_path(r'^upfiles/mod/',views.uploadmod, name='upload_mod'),
	re_path(r'^upfiles/modQC/',views.uploadmodqc, name='upload_modQC'),
	re_path(r'^upfiles/majQC/',views.uploadmajqc, name='upload_majQC'),
	re_path(r'^upfiles/maj/',views.uploadmaj, name='upload_maj'),
	re_path(r'^upfiles/dospat/([0-9]+)/',views.affdossier, name='Aff_dossier'),
	re_path(r'^upfiles/downOnce/([0-9]+)/',views.downOnce, name='donwnload_once'),
	re_path(r'^upfiles/downAll/([0-9]+)/',views.downAll, name='donwnload_all'),
]