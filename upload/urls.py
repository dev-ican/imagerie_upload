# -*-coding:Utf-8 -*

"""Chemin de l'application principal"""

from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('auth_in/', views.get_login, name='login'),
	path('form/', views.formulaire, name='form'),
	path('logout/', views.log_out, name='logout'),
	path('contact/', views.contact, name='contact'),
]