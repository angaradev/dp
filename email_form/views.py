from django.shortcuts import render
from .forms import EmailFormLight
from .models import EmailModel
from django.http import HttpResponseRedirect

def e_form_view(request):

    e_form = EmailFormLight(request.POST or None)
    if e_form.is_valid():
        phone = e_form.cleaned_data.get('phone')
        email_name = e_form.cleaned_data.get('email_name')
        callback, created = EmailModel.objects.get_or_create(phone=phone, name=email_name)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
