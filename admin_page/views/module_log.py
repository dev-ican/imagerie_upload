# -*-coding:Utf-8 -*

from django.utils import timezone
from upload.models import log, RefTypeAction


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
    log.objects.create(
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
    log.objects.create(
        user=user_current,
        action=type_action,
        date=date_now,
        info=info,
    )


def edition_log(req, info):
    """ Gère le log création """
    date_now = timezone.now()
    user_current = req.user
    info = user_current.username + info
    type_action = RefTypeAction.objects.get(pk=2)
    log.objects.create(
        user=user_current,
        action=type_action,
        date=date_now,
        info=info,
    )


def suppr_log(req, info):
    """ Gère le log création """
    date_now = timezone.now()
    user_current = req.user
    info = user_current.username + info
    type_action = RefTypeAction.objects.get(pk=3)
    log.objects.create(
        user=user_current,
        action=type_action,
        date=date_now,
        info=info,
    )
