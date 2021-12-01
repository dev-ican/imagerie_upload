from datetime import date

from django import forms
from django.core.validators import *
from django.http import *

from upload.models import *

CHOICES = [(0, "Collaborateurs"), (1, "Utilisateurs"), (2,"Administrateur service")]


class FormsEtude(forms.Form):
    """ Formulaire gérant les études """

    nom = forms.CharField(label="Nom de l'étude", max_length=100)
    date = forms.DateField(
        widget=forms.DateInput(
            format="%d/%m/%Y",
            attrs={"placeholder": "yyyy-mm-dd"},
        )
    )


class FormsEtape(forms.Form):
    """ Formulaire gérant les étapes """

    nom = forms.CharField(label="Nom de l'étape", max_length=100)
    '''etudes = forms.ChoiceField(
        widget=forms.Select(),
        choices=(["liste de vos études"]),
        required=True,
    )'''

class FormsEtapeEdit(forms.Form):
    """ Formulaire gérant les étapes """

    nom = forms.CharField(label="Nom de l'étape", max_length=100)
    etudes = forms.ChoiceField(
        widget=forms.Select(),
        choices=(["liste de vos études"]),
        initial='0',
    )

class FormsAutorisation(forms.Form):
    """ Formulaire gérant les authorisations """

    etude = forms.ChoiceField(
        widget=forms.Select(),
        choices=(["liste des études"]),
        initial="0",
    )
    centre = forms.ChoiceField(
        widget=forms.Select(),
        choices=(["liste des études"]),
        initial="0",
    )


class FormCentre(forms.Form):
    """ Formulaire gérant les centres """

    nom = forms.CharField(label="Nom  du centre", max_length=100)
    numero = forms.IntegerField(label="Numéro du centre")

class FormCentreEdit(forms.Form):
    """ Formulaire gérant les centres """

    nom = forms.CharField(label="Nom  du centre", max_length=100)
    numero = forms.IntegerField(label="Numéro du centre")
    date_ajout = forms.DateField(
        widget=forms.DateInput(
            format="%d/%m/%Y",
            attrs={"placeholder": "yyyy-mm-dd"},
        )
    )

class FormPwdChange(forms.Form):
    """Formulaire de modification des mots de passes"""

    email = forms.EmailField(
        label="Courriel de l'utilisateur",
        help_text='',
        max_length=200,
        validators=[EmailValidator()],
    )
    nw_mdp = forms.CharField(
        label="Nouveau Mot de passe",
        widget=forms.PasswordInput,
        max_length=100,
        validators=[
            RegexValidator(
                regex="([a-zA-Z]){4,12}([0-9]){2,12}",
                message="Mot de passe invalide",
            )
        ],
    )
    nw_mdp_second = forms.CharField(
        label="Répéter le mot de passe",
        widget=forms.PasswordInput,
        max_length=100,
        validators=[
            RegexValidator(
                regex="([a-zA-Z]){4,12}([0-9]){2,12}",
                message="Mot de passe invalide",
            )
        ],
    )

class FormsUser(forms.Form):
    """ Formulaire gérant les utilisateurs """

    username = forms.CharField(
        label="Identifiant de l'utilisateur", max_length=100
    )
    type = forms.ChoiceField(
        label="",
        choices=CHOICES,
        widget=forms.RadioSelect(
            attrs={"class": "d-inline-flex"}
        ),
    )
    email = forms.EmailField(
        label="Courriel de l'utilisateur",
        max_length=200,
        validators=[EmailValidator()],
    )
    nom = forms.CharField(
        label="Nom du Centre", max_length=100, required=False
    )
    numero = forms.IntegerField(
        label="Numero du Centre", required=False
    )
    pass_first = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput,
        max_length=100,
        validators=[
            RegexValidator(
                regex="([a-zA-Z]){4,12}([0-9]){2,12}",
                message="Mot de passe invalide",
            )
        ],
    )
    pass_second = forms.CharField(
        label="Répéter le mot de passe",
        widget=forms.PasswordInput,
        max_length=100,
        validators=[
            RegexValidator(
                regex="([a-zA-Z]){4,12}([0-9]){2,12}",
                message="Mot de passe invalide",
            )
        ],
    )


class FormsUserEdit(forms.Form):
    """ Formulaire gérant les éditions des utilisateurs """

    username = forms.CharField(
        label="Identifiant de l'utilisateur", max_length=100
    )
    type = forms.ChoiceField(
        label="",
        choices=CHOICES,
        widget=forms.RadioSelect(
            attrs={"class": "d-inline-flex"}
        ),
    )
    email = forms.EmailField(
        label="Courriel de l'utilisateur",
        max_length=200,
        validators=[EmailValidator()],
    )
    pass_first = forms.CharField(
        required=False,
        label="Mot de passe",
        widget=forms.PasswordInput,
        max_length=100,
        validators=[
            RegexValidator(
                regex="([a-zA-Z]){4,12}([0-9]){2,12}",
                message="Mot de passe invalide",
            )
        ],
    )
    pass_second = forms.CharField(
        required=False,
        label="Répéter le mot de passe",
        widget=forms.PasswordInput,
        max_length=100,
        validators=[
            RegexValidator(
                regex="([a-zA-Z]){4,12}([0-9]){2,12}",
                message="Mot de passe invalide",
            )
        ],
    )
