# Generated by Django 4.0.4 on 2022-06-22 06:33

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('upload', '0029_auto_20210503_1010'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Centre',
            new_name='RefInfoCentre',
        ),
    ]
