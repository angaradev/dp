from django.forms import ModelForm
from .models import AdGroups, Campaigns, Cars
from django import forms

class AdGroupForm(ModelForm):
    class Meta:
        model = AdGroups
        fields = '__all__'

class CarForm(ModelForm):
    car = forms.ChoiceField(choices=[(x.car_rus, x.car_rus) for x in Cars.objects.all()], required=False, label='',
            widget=forms.Select(attrs={'class': 'form-control-sm car-width',  'style': 'width: 300px;'}))
    class Meta:
        model = Cars
        fields = ('car',)


class CampFormSingle(forms.Form):
    camp_from = forms.ChoiceField(choices=[(x.id, x.camp_name) for x in Campaigns.objects.all()], required=False,
            label='Выбрать кампанию для копирования from',
            widget=forms.Select(attrs={'class': 'form-control-sm car-width',  'style': 'width: 300px;'}))

class CampEditForm(ModelForm):
    class Meta:
        model = Campaigns
        fields = '__all__'
    
class CampCreateForm(ModelForm):
    class Meta:
        model = Campaigns
        fields = ('car', 'camp_name')
    
