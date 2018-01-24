from django import forms
from django.core.validators import MinLengthValidator


class UrlForm(forms.Form):
    url = forms.CharField(validators=[MinLengthValidator(32)], max_length=33, label="URL")

