from django import forms
from .models import EmailModel


# class EmailForm(forms.Form):
#     name = forms.CharField(label='Ваше Имя')
#     phone = forms.CharField(label='Ваш Nелефон')
#     email = forms.CharField(label='Ваш e-mail')
#     text = forms.CharField(widget=forms.Textarea, label='Ваше сообщение')
#
class EmailFormLight(forms.Form):
    name = forms.CharField(label='Ваше Имя', required=False)
    phone = forms.CharField(label='Ваш телефон')


class EmailFormOneField(forms.Form):
    phone = forms.CharField(label='Ваш телефон')

