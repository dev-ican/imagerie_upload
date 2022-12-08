from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class LogIn(forms.Form):
    ''' Formulaire de connexion à l'application '''
    log_id = forms.CharField(label="Identifiant", max_length=100)
    pwd = forms.CharField(label="Mot de passe",
                          widget=forms.PasswordInput(),
                          max_length=100,
                          )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())