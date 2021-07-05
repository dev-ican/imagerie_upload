# Generated by Django 3.0.7 on 2021-04-27 06:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('upload', '0020_auto_20201029_1102'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefEtatValide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='RefEtatValideCompte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='ValideCompte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_demande', models.DateTimeField(verbose_name='Date de la demande')),
                ('date_validation', models.DateTimeField(verbose_name='Date de validation')),
                ('compte_valide', models.ForeignKey(db_column='Compte_Valider', on_delete=django.db.models.deletion.CASCADE, related_name='Compte_Valider', to=settings.AUTH_USER_MODEL)),
                ('demandeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('etat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload.RefEtatValideCompte')),
            ],
        ),
    ]
