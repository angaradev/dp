from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Categories, Products
from django.db.models import Count, Sum
from django.db.models import Subquery 
from products.views import categories_tree, get_image_path
import os
from django.conf import settings 


def get_image_path_all(obj):
    working_dir = settings.STATICFILES_DIRS[1] 
    files  =  os.listdir(os.path.join(working_dir, obj.cat_n))[:10]
    img_list = []
    for f in files:
        img_list.append(os.path.join(obj.cat_n, f))
    setattr(obj, 'image_path', img_list ) 
    return obj

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

def show_cars():
    qs = Products.objects.values('car').annotate(dcount=Count('car'))
    return qs

@login_required
def admin_photos_view(request):
    car = request.GET.get('car')
    qs = Categories.objects.filter(id__gt=99, id__lt=999)
    objects = [] 
    for q in qs:
        sub_l = []
        sub = Categories.objects.filter(parent_id=q.id)
        for s in sub:
            sub_l.append(s.id)
        pqs = Products.objects.filter(cat__in=sub_l)
        if car is not None:
            pqs = Products.objects.filter(cat__in=sub_l, car=car)
        if not pqs:
            continue
        objects.append({'id': q.id, 'name': q.name, 'p_count': pqs.count()})

    cars = show_cars()
    if not car:
        car = None

    context = {
                'objects': objects,
                'cars': cars,
                'single_car': car,
            }
    return render(request, 'admin/photo.html', context)


@login_required
def admin_photos_statistic(request):
    context = {

            }
    return render(request, 'admin/statistic.html', context)



@login_required
def admin_photo_listing(request, pk):
    car = request.GET.get('car')
    
    cat = categories_tree(pk)
    li = []
    for c in cat:
        li.append(c.id)
    if car is not None:
        qs = Products.objects.filter(cat__in=li, car=car)
    else:
        qs = Products.objects.filter(cat__in=li)
    objects = get_image_path(qs)
    
    context = {
                'objects': objects,

            }
    return render(request, 'admin/photo_listing.html', context)
