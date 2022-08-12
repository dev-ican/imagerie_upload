# from datetime import date
from django import forms
from django.contrib.auth.models import User
from django.core.validators import *
# from django.http import *
from upload.models import RefEtudes, RefInfoCentre
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


CHOICES = [(0, "Collaborateurs"),
           (1, "Utilisateurs"),
           (2,"Administrateur service")
           ]
           

class FormsEtude(forms.Form):
    """ Formulaire gérant les études """

    nom = forms.CharField(label="Nom de l'étude", max_length=100)
    date = forms.DateField(widget=forms.DateInput(
            format="%Y-%m-%d",
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
        choices=(["liste des centres"]),
        initial="0",
        )


class FormCentre(forms.Form):
    """ Formulaire gérant les centres """

    nom = forms.CharField(label="Nom  du centre", max_length=100)
    numero = forms.IntegerField(label="Numéro du centre")


class FormCentreEdit(forms.Form):
    """ Formulaire gérant les centres """

    users = User.objects.filter(is_staff=False).filter(is_superuser=False)
    centres = RefInfoCentre.objects.all()

    choix_utilisateurs = []

    for user in users:
        choix_utilisateurs.append((user.id, user.username))


    nom = forms.CharField(label="Nom  du centre", max_length=100)
    numero = forms.IntegerField(label="Numéro du centre")
    utilisateurs = forms.MultipleChoiceField(label="Utilisateurs rattachés au centre",
                                             widget=forms.Select(),
                                             choices=choix_utilisateurs)
    date_ajout = forms.DateField(
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"placeholder": "yyyy-mm-dd"},
        )
    )


class FormPwdChange(forms.Form):
    """Formulaire de modification des mots de passe"""

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

    centres = RefInfoCentre.objects.all()
    choice_centre = []
    for centre in centres:
        choice_centre.append((centre.id, centre.nom))

    username = forms.CharField(label="Identifiant de l'utilisateur", max_length=100)
    
    type = forms.ChoiceField(label="",
                            choices=CHOICES,
                            widget=forms.RadioSelect(
                            attrs={"class": "d-inline-flex"}
                            ))

    email = forms.EmailField(label="Courriel de l'utilisateur",
                             max_length=200,
                             validators=[EmailValidator()],
                            )

    centre = forms.ChoiceField(widget=forms.Select(),
                                     label="Centre :", 
                                     choices=choice_centre,
                                     initial="4",
                                     )

    # nom = forms.CharField(label="Nom du Centre",
    #                       max_length=100,
    #                       required=False
    #                      )

    # numero = forms.IntegerField(label="Numero du Centre",
    #                             required=False
    #                            )

    pass_first = forms.CharField(label="Mot de passe",
                                 widget=forms.PasswordInput,
                                 max_length=100,
                                 validators=[RegexValidator(regex="([a-zA-Z]){4,12}([0-9]){2,12}",
                                                            message="Mot de passe invalide",
                                                            )])

    pass_second = forms.CharField(label="Répéter le mot de passe",
                                  widget=forms.PasswordInput,
                                  max_length=100,
                                  validators=[RegexValidator(regex="([a-zA-Z]){4,12}([0-9]){2,12}",
                                                             message="Mot de passe invalide",
                                                            )])


class FormsUserEdit(forms.Form):
    """ Formulaire gérant les éditions des utilisateurs """

    username = forms.CharField(label="Identifiant de l'utilisateur",
                               max_length=100
                               )

    type = forms.ChoiceField(label="",
                             choices=CHOICES,
                             widget=forms.RadioSelect(
                                    attrs={"class": "d-inline-flex"}
                             ))

    email = forms.EmailField(label="Courriel de l'utilisateur",
                             max_length=200,
                             validators=[EmailValidator()]
                             )

    pass_first = forms.CharField(required=False,
                                 label="Mot de passe",
                                 widget=forms.PasswordInput,
                                 max_length=100,
                                 validators=[RegexValidator(regex="([a-zA-Z]){4,12}([0-9]){2,12}",
                                                            message="Mot de passe invalide",
                                                            )])

    pass_second = forms.CharField(required=False,
                                  label="Répéter le mot de passe",
                                  widget=forms.PasswordInput,
                                  max_length=100,
                                  validators=[RegexValidator(regex="([a-zA-Z]){4,12}([0-9]){2,12}",
                                                             message="Mot de passe invalide"
                                                             )])


class FormSelectionEtudeEtape(forms.Form):
    """Formulaire permettant de séléctionner un centre et une étude afin d'afficher les données"""

    etudes = RefEtudes.objects.all()
    choice_etude = []
    for etude in etudes:
        choice_etude.append((etude.id, etude.nom))

    centres = RefInfoCentre.objects.all().order_by("numero")
    choice_centre = []
    for centre in centres:
        centre_nom_num = f"{centre.numero}_{centre.nom}"
        choice_centre.append((centre.id, centre_nom_num))

    etude_choice = forms.ChoiceField(widget=forms.Select(),
                                     label="", 
                                     choices=choice_etude,
                                     initial="4",
                                     )

    centre_choice = forms.ChoiceField(widget=forms.Select(),
                                      label="",
                                      choices=choice_centre,
                                      initial="5",
                                      )


class FormSelectionEtudeURC(forms.Form):
    """Formulaire permettant de séléctionner un centre et une étude afin d'afficher les données"""

    choice_etude = [(4, 'OPTIM')]

    centres = RefInfoCentre.objects.all()
    choice_centre = []
    for centre in centres:
        choice_centre.append((centre.id, centre.nom))

    etude_choice = forms.ChoiceField(widget=forms.Select(),
                                    label="", 
                                    choices=choice_etude,
                                    )

    centre_choice = forms.ChoiceField(widget=forms.Select(),
                                    label="",
                                    choices=choice_centre,
                                    initial="5",
                                    )
