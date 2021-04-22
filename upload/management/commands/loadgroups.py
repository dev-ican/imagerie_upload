from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

import requests
import json
import unicodedata

class Command(BaseCommand):
    help = "Importation des groupes de l'application"

    def handle(self, *args, **options):
        list_groups=["Utilisateurs", "Collaborateurs", "Administrateur", "Administrateur service"]

        for item in list_groups:
            new_group, created = Group.objects.get_or_create(name=item)

        self.stdout.write(self.style.SUCCESS('commande succes'))