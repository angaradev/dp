from django.forms import ModelForm
from .models import AdGroups

class AdGroupForm(ModelForm):
    class Meta:
        model = AdGroups
        fields = '__all__'


