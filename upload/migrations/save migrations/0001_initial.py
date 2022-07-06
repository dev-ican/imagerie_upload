# Generated by Django 3.0.7 on 2020-08-21 08:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JonctionUtilisateurEtude',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_autorisation', models.DateTimeField(verbose_name="Date d'autorisation")),
            ],
        ),
        migrations.CreateModel(
            name='RefControleQualite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='RefEtatEtape',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='RefEtudes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=5000)),
                ('date_ouverture', models.DateTimeField(verbose_name="Date d'ouverture")),
            ],
        ),
        migrations.CreateModel(
            name='SuiviUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_patient', models.CharField(max_length=5000)),
                ('date_upload', models.DateTimeField(verbose_name="Date d'envois")),
                ('date_examen', models.DateTimeField(verbose_name='Date examen')),
                ('controle_qualite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload.RefControleQualite')),
                ('etude', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload.JonctionUtilisateurEtude')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Centre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=5000)),
                ('numero', models.FloatField()),
                ('date_ajout', models.DateTimeField(verbose_name="Date d'ajout")),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RefEtapeEtude',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=5000)),
                ('etude', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload.RefEtudes')),
            ],
        ),
        migrations.AddField(
            model_name='jonctionutilisateuretude',
            name='etude',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload.RefEtudes'),
        ),
        migrations.AddField(
            model_name='jonctionutilisateuretude',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='JonctionEtapeSuivi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name="Date de l'étape")),
                ('etape', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload.RefEtapeEtude')),
                ('etat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload.RefEtatEtape')),
                ('upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload.SuiviUpload')),
            ],
        ),
    ]

    