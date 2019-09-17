from django.shortcuts import render
from .models import Products, Categories
from django.db.models import Count, Min, Max
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings
import os

def show_cars():
    qs = Products.objects.values('car').annotate(dcount=Count('car'))
    return qs

def show_brands(pk, car, cat):
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
    qs = Products.objects.filter(car=car).order_by('?')[:50]
    cats_tmp = Categories.objects.filter(parent_id=0)
    cats = []
    for c in cats_tmp:
        nums = Products.objects.filter(car=car, cat__in=categories_tree(c.id)).count()
        if nums != 0:
            setattr(c, 'prod_count', nums)
            cats.append(c)
    context = {
            'objects': qs,
            'cars': show_cars(),
            'categories': cats,
            'single_car': car,
            }
    return render(request, 'products/newparts.html', context)

def cars_subcats(request, car, slug, **kwargs):
    brand = request.GET.get('brand', None)
    cats_tmp = Categories.objects.get(slug=slug)
    second_level_cats = Categories.objects.filter(parent_id=cats_tmp.id)
    cats = []
    for c in second_level_cats:
        nums = Products.objects.filter(car=car, cat__in=categories_tree(c.id)).count()
        if nums != 0:
            setattr(c, 'prod_count', nums) 
            cats.append(c)

    cats_list = [] 
    if len(cats) == 0:
        if brand:
            qs = Products.objects.filter(car=car, cat=cats_tmp.id, brand=brand)
        else:
            qs = Products.objects.filter(car=car, cat=cats_tmp.id)
    else:
        for c in cats:
            cats_list.append(c.id)
        groups = Categories.objects.filter(parent_id__in=cats_list)
        for g in groups:
            cats_list.append(g.id) 
        if brand:
            qs = Products.objects.filter(car=car, cat__in=cats_list, brand=brand)
        else:
            qs = Products.objects.filter(car=car, cat__in=cats_list)
    
    brands = qs.values('brand').annotate(brand_count=Count('brand')) 
    h1 = cats_tmp.name
    try:
        p = Paginator(qs, 20)
        page = request.GET.get('page')
        objects = p.get_page(page)
    except:
        pass
    if request.GET.get('load_all') == 'all':
        objects = qs
    
    def get_image_path():
        working_dir = '/media/manhee/b68fbbb8-c6b6-4d26-8c3a-a9b68dbc2eb3/ducatoparts_photo_ebay'
        try:
            for obj in objects:
                files  =  os.listdir(os.path.join(working_dir, obj.cat_n))
                setattr(obj, 'image_path', os.path.join(obj.cat_n, files[0])) 
        except:
            pass
    get_image_path()

            

    context = {
            'objects': objects,
            'cars': show_cars(),
            'categories': cats,
            'single_car': car,
            'brands': brands,
            'title_h1': h1,
            'car': car,
            'brand': brand,
            }
    
    return render(request, 'products/newparts.html', context)
