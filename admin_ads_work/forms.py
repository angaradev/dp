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
