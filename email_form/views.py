from django.shortcuts import render
from .forms import EmailFormLight
from .models import EmailModel
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
import re


def e_form_view(request):

    e_form = EmailFormLight(request.POST or None)
    if e_form.is_valid():
        phone = e_form.cleaned_data.get('phone')
        email_name = e_form.cleaned_data.get('email_name')
        callback, created = EmailModel.objects.get_or_create(phone=phone, name=email_name)
        send_mail(
            'Заказ звонка с Ducatoparts.ru',
            f'Пришел запрос на обратный звонок. Телефон - {phone}. Имя - {email_name}',
            settings.SHOP_EMAIL_FROM,
            settings.SHOP_EMAILS_MANAGERS,
            fail_silently=False,
        )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def footer_form(request):
    phone = request.POST.get('phone')
    if phone:
        phone = re.sub(r'[^\d]', '', phone)
        callback, created = EmailModel.objects.get_or_create(phone=phone)
        send_mail(
            'Заказ звонка с Ducatoparts.ru',
            f'Пришел запрос на обратный звонок. Телефон - {phone}',
            settings.SHOP_EMAIL_FROM,
            settings.SHOP_EMAILS_MANAGERS,
            fail_silently=False,
        )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

