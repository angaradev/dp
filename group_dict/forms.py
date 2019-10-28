from django import forms
from products.models import Categories


class KeyWordForm(forms.Form):
    group_name = forms.CharField(label='Название группы')
    parent = forms.ModelChoiceField(queryset=Categories.objects.filter(id__gt=99, id__lt=999).order_by('name'))
    plus = forms.CharField(label='Плюс слова', widget=forms.Textarea(attrs={'rows': 5}))
    minus = forms.CharField(label='Минус слова', widget=forms.Textarea(attrs={'rows': 5}), required=False)
    
    
