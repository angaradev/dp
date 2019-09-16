from django.shortcuts import render
from .models import Products, Categories
from django.db.models import Count, Min, Max
from django.db.models import Q

def show_cars():
    qs = Products.objects.values('car').annotate(dcount=Count('car'))
    return qs

def show_brands(pk, **kwargs):
    for k, v in kwargs.items():
        pass
    qs = Products.objects.filter(cat = 2502).values('brand').annotate(dbrand=Count('brand'))
    return qs

def show_price(price_min, price_max):
    price_range = Products.objects.filter(price__range=[price_min, price_max])
    p_min = Products.objects.all().aggregate(Min('price'))
    p_max = Products.objects.all().aggregate(Max('price'))
    return p_min, p_max, price_range

def categories_tree(pk):

    if pk > 999:
        cats = Categories.objects.filter(id=pk)
    if pk < 999 and pk > 99:
        cats = Categories.objects.filter(parent_id=pk)
    if pk < 99:
        cats_sub = Categories.objects.filter(parent_id=pk)
        c_l = []
        for cat_sub in cats_sub:
            c_l.append(cat_sub.id)
        cats = Categories.objects.filter(parent_id__in=c_l)
    return cats        
    


def newparts(request):

    qs = Products.objects.all()[:20]
    cats = Categories.objects.filter(parent_id=0)
    context = {
            'objects': qs, 
            'categories': cats,
            'cars': show_cars(),
           # 'brands': show_brands(),
            }
    return render(request, 'products/newparts.html', context)

def subcat(request, pk):

    cars = show_cars()
    cats = Categories.objects.filter(parent_id=pk)
    if pk > 999:
        qs = Products.objects.filter(cat=pk)[:20]
    elif pk > 99 and pk < 999:
        cats = Categories.objects.filter(parent_id=pk)
        # Getting products from those parent catrgories
        ids = []
        for cat in cats:
            ids.append(cat.id)
        qs = Products.objects.filter(cat__in=ids)[:20]

    elif pk < 99:
        ids = []
        for cat in cats:
            ids.append(cat.id)
        qs = Products.objects.filter(cat__in=ids)[:20]
        scats = Categories.objects.filter(parent_id__in=ids)
        sids = []
        for sid in scats:
            sids.append(sid.id)

        qs = Products.objects.filter(cat__in=sids)[:20]
    p_min, p_max, price_range = show_price(4600, 5000)
    context = {
            'objects': qs,
            'categories': cats,
            'cars': cars,
            'brands': show_brands(pk),
            'price_range': price_range,
            'p_min': p_min,
            'p_max':p_max,
            }
    return render(request, 'products/newparts.html', context)


def cars(request, car):
    qs = Products.objects.filter(car=car)
    print(qs.count())
    cats = Categories.objects.filter(parent_id=0).annotate(prod_count=Count('cat'))
    context = {
            'objects': qs,
            'cars': show_cars(),
            'categories': cats,
            'single_car': car,
            }
    return render(request, 'products/newparts.html', context)

def cars_subcats(request,car, slug):
    cats = Products.objects.filter(car=car).annotate(Count('cat')) 
    cats_list = [] 
    for c in cats:
        cats_list.append(c.id)
    qs = Products.objects.filter(car=car, cat__in=cats_list)
    context = {
            'objects': qs,
            'cars': show_cars(),
            'categories': cats,
            'single_car': car
            }
    
    return render(request, 'products/newparts.html', context)
