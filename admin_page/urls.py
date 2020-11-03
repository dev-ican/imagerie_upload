# -*-coding:Utf-8 -*

"""Chemin de l'application principal"""

from django.urls import path, re_path

from . import views

urlpatterns = [
	path('', views.admin_page, name='admin'),
	path('etudes/', views.admin_etude, name='admin_etude'),
	re_path(r'^etudes/edit/([0-9]+)/',views.etude_edit, name='etude_edit'),
	re_path(r'^etudes/delete/([0-9]+)/',views.etude_del, name='etude_suppr'),	
	path('etapes/', views.admin_etape, name='admin_etape'),
	re_path(r'^etapes/edit/([0-9]+)/',views.etape_edit, name='etape_edit'),
	re_path(r'^etapes/delete/([0-9]+)/',views.etape_del, name='etape_suppr'),
	path('viewUser/', views.admin_user, name='admin_utilisateur'),
	re_path(r'^viewUser/edit/([0-9]+)/',views.user_edit, name='user_edit'),
	re_path(r'^viewUser/delete/([0-9]+)/',views.user_del, name='user_suppr'),
	path('centre/', views.admin_centre, name='admin_centre'),
	re_path(r'^centre/edit/([0-9]+)/',views.centre_edit, name='centre_edit'),
	re_path(r'^centres/delete/([0-9]+)/',views.centre_del, name='centre_suppr'),
	path('userAuth/', views.admin_auth, name='admin_autorisation'),
	re_path(r'^userAuth/edit/([0-9]+)/',views.auth_edit, name='auth_edit'),
	re_path(r'^userAuth/delete',views.auth_del, name='auth_suppr'),
	path('upfiles/', views.admin_up, name='admin_upload'),
	re_path(r'^upfiles/tris/([0-9]+)/',views.upload_tris, name='upload_tris'),
	re_path(r'^upfiles/mod/',views.upload_mod, name='upload_mod'),
	re_path(r'^upfiles/modQC/',views.upload_mod_qc, name='upload_modQC'),
	re_path(r'^upfiles/majQC/',views.upload_maj_qc, name='upload_majQC'),
	re_path(r'^upfiles/maj/',views.upload_maj, name='upload_maj'),
	re_path(r'^upfiles/dospat/([0-9]+)/',views.aff_dossier, name='Aff_dossier'),
	re_path(r'^upfiles/downOnce/([\w\d\D]+)',views.down_once, name='donwnload_once'),
	re_path(r'^upfiles/downAll/([0-9]+)/',views.down_all, name='donwnload_all'),
	re_path(r'^upfiles/walk_up/',views.walk_up, name='walk_up'),
	re_path(r'^upfiles/walk_return/',views.walk_down, name='walk_return'),
]