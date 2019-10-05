from django.shortcuts import render, redirect
from django.core.mail import send_mail
from products.models import Categories, Products, Cart
from products.views import get_image_path
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

    brakes = get_image_path(brakes)
    fuel = get_image_path(fuel)
    engine = get_image_path(engine)
    body = get_image_path(body)
    
    cart = None
    if request.session.get('cart_id', None):
        cart = Cart.objects.get(id=request.session.get('cart_id'))

    context = {
            'brakes': brakes,
            'fuel': fuel,
            'body': body,
            'engine': engine,
            'articles': articles,
            'categories': cats,
            'cars': cars,
            'cart': cart,
            }

    return render(request, 'home/home.html', context)

def about(request):
    form = EmailFormLight(request.POST or None)

    if form.is_valid():

        phone = form.cleaned_data.get('phone')
        name = form.cleaned_data.get('name')
        callback, created = EmailModel.objects.get_or_create(phone=phone, name=name)
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


def footer_form(request):
    phone = request.POST.get('phone')
    if phone:
        callback, created = EmailModel.objects.get_or_create(phone=phone)
        send_mail('Anon', 'Заявка', 'yellkalolka', ['yellkalolka@gmail.com'], fail_silently=False,)
    return redirect('home')
