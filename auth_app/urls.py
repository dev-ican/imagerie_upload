# -*-coding:Utf-8 -*

"""Chemin de l'application principal"""

from django.urls import path

from . import views

urlpatterns = [
	path('auth_in/', views.get_login, name='login'),
	path('logout/', views.log_out, name='logout'),
]