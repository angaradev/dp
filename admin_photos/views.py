from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Categories, Products
from django.db.models import Count, Sum
from django.db.models import Subquery 



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
    context = {
                'objects': objects,
                'car': car,
            }
    return render(request, 'admin/photo.html', context)


@login_required
def admin_photos_statistic(request):
    context = {

            }
    return render(request, 'admin/statistic.html', context)
