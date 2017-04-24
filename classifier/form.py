from django import forms
from django.core.validators import MinLengthValidator

"""入力フォールの形式を指定"""
class UrlForm(forms.Form):
    url = forms.CharField(validators=[MinLengthValidator(32)], max_length=33, label="URL")

