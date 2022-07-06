# Generated by Django 3.0.7 on 2021-04-27 08:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('upload', '0025_auto_20210427_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='validecompte',
            name='validateur',
            field=models.OneToOneField(blank=True, db_column='validateur', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='validateur', to=settings.AUTH_USER_MODEL),
        ),
    ]