from django.shortcuts import render, redirect
from django.core.mail import send_mail
from products.models import Categories, Products
from blogs.models import Blogs
from email_form.forms import EmailFormLight, EmailFormOneField
from email_form.models import EmailModel
from django.db.models import Count, Min, Max
from django.conf import settings


def home(request):
    ls = settings.SALES_ON_HOME 
    brakes = Products.objects.filter(id__in=ls['brakes'])
    fuel = Products.objects.filter(id__in=ls['fuel'])
    body = Products.objects.filter(id__in=ls['body'])
    engine = Products.objects.filter(id__in=ls['engine'])
    articles = Blogs.objects.all().order_by('-publish')[:2]
    cars = Products.objects.values('car').annotate(dcount=Count('car'))

    cats = Categories.objects.filter(parent_id=0)

    context = {
            'articles': articles,
            'categories': cats,
            'cars': cars,
            'brakes': brakes,
            'fuel': fuel,
            'body': body,
            'engine': engine,
                       }

    return render(request, 'home/home.html', context)


def reviews(request):
    form = EmailFormLight(request.POST or None)

    if form.is_valid():

        phone = form.cleaned_data.get('phone')
        name = form.cleaned_data.get('name')
        callback, created = EmailModel.objects.get_or_create(phone=phone, name=name)
        return redirect('tankyoucall')
    context = {
        'form': form,

            }
    return render(request, 'home/reviews.html', context)


def about(request):
    form = EmailFormLight(request.POST or None)

    if form.is_valid():

        phone = form.cleaned_data.get('phone')
        name = form.cleaned_data.get('name')
        callback, created = EmailModel.objects.get_or_create(phone=phone, name=name)
        return redirect('tankyoucall')
    context = {
        'form': form,

            }
    return render(request, 'home/about.html', context)

def payment(request):
    context = {

            }
    return render(request, 'home/payment.html', context)

def delivery(request):
    form = EmailFormLight(request.POST or None)

    if form.is_valid():

        phone = form.cleaned_data.get('phone')
        name = form.cleaned_data.get('name')
        callback, created = EmailModel.objects.get_or_create(phone=phone, name=name)
        return redirect('tankyoucall')

    context = {
        'form': form,
            }
    return render(request, 'home/delivery.html', context)

def guaranties(request):
    context = {

            }
    return render(request, 'home/guaranties.html', context)

def policy(request):
    context = {

            }
    return render(request, 'home/policy.html', context)

def contacts(request):
    context = {

            }
    return render(request, 'home/contacts.html', context)

def requsites(request):
    context = {

            }
    return render(request, 'home/requsites.html', context)

def thankyoucall(request):
    return render(request, 'home/thank_you.html')
