from django import forms
from .models import Orders
from django.conf import settings



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

class PaymentForm(forms.Form):

    shopId = forms.IntegerField(widget = forms.HiddenInput(), required = True, initial=settings.PAYMENT_SHOP_ID)
    scid = forms.IntegerField(widget = forms.HiddenInput(), required = True, initial=settings.PAYMENT_SHOP_SCID)
    sum  = forms.DecimalField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Сумма Заказа')
    customerNumber = forms.CharField(required=True, label="Введите Номер Телефона")
    orderDetails = forms.CharField(widget=forms.Textarea(attrs={'rows': 5,}),
            label="Дополнительный комментарий к заказу",
            required=False)
    
    
