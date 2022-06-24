# -*-coding:Utf-8 -*

from django.utils import timezone
from upload.models import Log, RefTypeAction


# Gestion log
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------


def information_log(req, info):
    """ Gère le log Informations """
    date_now = timezone.now()
    user_current = req.user
    info = user_current.username + info
    type_action = RefTypeAction.objects.get(pk=4)
    Log.objects.create(
        user=user_current,
        action=type_action,
        date=date_now,
        info=info,
    )


def creation_log(req, info):
    """ Gère le log création """
    date_now = timezone.now()
    user_current = req.user
    info = user_current.username + info
    type_action = RefTypeAction.objects.get(id=7)
    Log.objects.create(
        user=user_current,
        action=type_action,
        date=date_now,
        info=info,
    )


def edition_log(req, info):
    """ Gère le log édition """
    date_now = timezone.now()
    user_current = req.user
    info = user_current.username + info
    type_action = RefTypeAction.objects.get(pk=2)
    Log.objects.create(
        user=user_current,
        action=type_action,
        date=date_now,
        info=info,
    )


def suppr_log(req, info):
    """ Gère le log suppression """
    date_now = timezone.now()
    user_current = req.user
    info = user_current.username + info
    type_action = RefTypeAction.objects.get(pk=3)
    Log.objects.create(
        user=user_current,
        action=type_action,
        date=date_now,
        info=info,
    )
