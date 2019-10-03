from django import forms
from .models import Orders




class OrderForm(forms.ModelForm):
    phone = forms.CharField(label='')
    email = forms.EmailField(required=False, label='')
    address = forms.CharField(required=False, label='')
    comments = forms.CharField(widget=forms.Textarea, required=False, label='')
    cart = forms.CharField(required=False)
    
    class Meta:
        model = Orders
        fields = [
                'email',
                'phone',
                'address',
                'comments',
                'cart',
                ]


