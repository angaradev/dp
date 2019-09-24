from django.shortcuts import render
from products.models import Categories, Products



def home(request):
    ls = {'brakes': [2774, 2582, 2560, 2027], 'fuel': [1596, 3160, 1556, 1529], 'body': [2257, 2252, 3508, 3757], 'engine': [3136, 3035, 1932, 1027]}

    brakes = Products.objects.filter(id__in=ls['brakes'])
    fuel = Products.objects.filter(id__in=ls['fuel'])
    body = Products.objects.filter(id__in=ls['body'])
    engine = Products.objects.filter(id__in=ls['engine'])

    context = {
            'brakes': brakes,
            'fuel': fuel,
            'body': body,
            'engine': engine,
            }

    return render(request, 'home/home.html', context)
