from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.clickjacking import xframe_options_exempt

from django.conf import settings
from io import StringIO, BytesIO

from django.db.models import Count, Q
import json
import zipfile
import os, tempfile
from wsgiref.util import FileWrapper
from .module_views import *

from datetime import date, time, datetime
from django.utils import timezone
from .module_admin import checkmdp, take_data, choiceEtude, choiceCentre

from admin_page.forms import FormsEtude, FormsEtape, FormsAutorisation, FormsUser, FormsUserEdit, FormCentre
from upload.models import RefEtudes, JonctionUtilisateurEtude, RefEtapeEtude, RefInfocentre, JonctionEtapeSuivi, SuiviUpload, DossierUpload, RefEtatEtape, RefControleQualite, log, RefTypeAction

# Gestion log
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------

def informationLog(req, info):
	''' Gère le log Informations '''
	date_now = timezone.now()
	user_current = req.user
	info = user_current.username + info
	type_action = RefTypeAction.objects.get(pk=4)
	log.objects.create(user=user_current, action=type_action, date=date_now, info=info)

def creationLog(req, info):
	''' Gère le log création '''
	date_now = timezone.now()
	user_current = req.user
	info = user_current.username + info
	type_action = RefTypeAction.objects.get(pk=7)
	log.objects.create(user=user_current, action=type_action, date=date_now, info=info)

def editionLog(req, info):
	''' Gère le log création '''
	date_now = timezone.now()
	user_current = req.user
	info = user_current.username + info
	type_action = RefTypeAction.objects.get(pk=2)
	log.objects.create(user=user_current, action=type_action, date=date_now, info=info)

def supprLog(req, info):
	''' Gère le log création '''
	date_now = timezone.now()
	user_current = req.user
	info = user_current.username + info
	type_action = RefTypeAction.objects.get(pk=3)
	log.objects.create(user=user_current, action=type_action, date=date_now, info=info)




