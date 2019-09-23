from django import forms



class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }), label='* ИМЯ ПОЛЬЗОВАТЕЛЯ')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',}), label='* ПАРОЛЬ')

