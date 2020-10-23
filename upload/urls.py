# -*-coding:Utf-8 -*

"""Chemin de l'application principal"""

from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('form/', views.formulaire, name='formulaire')
]