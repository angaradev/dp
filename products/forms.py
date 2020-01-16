from django import forms
from .models import Orders
from django.conf import settings
from django.core.exceptions import NON_FIELD_ERRORS



class OrderForm(forms.ModelForm):
    messages = {
            'required': 'Пожалуйста напишите телефон для связи!',
            'invalid': 'Пожалуйста напишите EMAIL для связи!',
            }

    phone = forms.CharField(label='', error_messages={'required': 'Enter some telephone please'})
    email = forms.EmailField(required=True, label='')
    address = forms.CharField(required=False, label='')
    comments = forms.CharField(widget=forms.Textarea, required=False, label='')
    cart = forms.CharField(required=False)

    def clean(self):
            phone = self.cleaned_data.get('phone')
            if not phone:
                raise forms.ValidationError('Invalid Login : I want to change this CSS')
            return self.cleaned_data
    
    class Meta:
        model = Orders
        fields = '__all__'
        error_messages = {
                'email': {
                    'invalid': 'Пожалуйста напишите телефон для связи!',
                    },
                        
                }

class PaymentForm(forms.Form):

    shopId = forms.IntegerField(widget = forms.HiddenInput(), required = True, initial=settings.PAYMENT_SHOP_ID)
    scid = forms.IntegerField(widget = forms.HiddenInput(), required = True, initial=settings.PAYMENT_SHOP_SCID)
    sum  = forms.DecimalField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Сумма Заказа')
    customerNumber = forms.CharField(required=True, label="Введите Номер Телефона")
    orderDetails = forms.CharField(widget=forms.Textarea(attrs={'rows': 5,}),
            label="Дополнительный комментарий к заказу",
            required=False)
    
    
