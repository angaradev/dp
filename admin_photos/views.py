from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from products.models import Categories, Products
from django.db.models import Count, Sum
from django.db.models import Subquery 
from products.views import categories_tree, get_image_path
import os
from django.conf import settings 
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Q
from django.urls.base import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PhotoStatistic




@login_required
def make_stat(request):
    qs = Products.objects.values('img_check')
    print(count(qs))
    return redirect('home')


class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        
        d = Products.objects.values('img_check')
        print(d)
        checked = d.filter(img_check=True).count()
        unchecked = d.filter(img_check=False).count()
        labels = [f'Сделано {checked}', f'Осталось {unchecked}']
        defaultData = [checked, unchecked]



        data = {
                "labels": labels,   #['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                'defaultData':defaultData, # [12, 19, 3, 5, 2, 3],
                "bgColors": [
                                'rgba(0, 255, 127, 0.2)',
                                'rgba(255, 20, 147, 0.2)',
                            ],
                "borderColor":  [
                                'rgba(0, 255, 127, 1)',
                                'rgba(255, 20, 147, 1)',
                            ]
                }
        return Response(data)      

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

    checked = request.GET.get('checked')
    car = request.session.get('car', None)
    qs = Categories.objects.filter(id__gt=99, id__lt=999)
    objects = [] 
    for q in qs:
        sub_l = []
        sub = Categories.objects.filter(parent_id=q.id)
        for s in sub:
            sub_l.append(s.id)
        if checked and checked == 'True':
            pqs = Products.objects.filter(cat__in=sub_l).filter(img_check=True).distinct()
        elif checked and checked == 'False':
            pqs = Products.objects.filter(cat__in=sub_l).filter(img_check=False).distinct()
        else:
            pqs = Products.objects.filter(cat__in=sub_l).distinct()

        if not pqs:
            continue
        objects.append({'id': q.id, 'name': q.name, 'p_count': pqs.count(), 'checked_count':
            pqs.filter(img_check=True).count(), 'unchecked_count': pqs.filter(img_check=False).count()})

    cars = show_cars()

    context = {
                'objects': objects,
                'cars': cars,
                'car': car,
                'checked': checked,
            }
    return render(request, 'admin/photo.html', context)





@login_required
def admin_photo_listing(request, pk):

    car = request.GET.get('car')
    checked = request.GET.get('checked')

    cat = categories_tree(pk)
    li = []
    for c in cat:
        li.append(c.id)
    qs = Products.objects.filter(cat__in=li).distinct()

    if not car or not checked:
        car = 'all'
        checked = 'All'
        
    if car == 'all' and checked == 'All':
        pqs = qs
    elif (car and car != 'all') and (checked and checked != 'All'):
        pqs = qs.filter(car=car).filter(img_check=checked).distinct()
    elif car != 'all' and (checked == 'All' or checked is None):
        pqs = qs.filter(car=car).distinct()
    elif car == 'all' and (checked and checked != 'All'):
        print('in here', checked)
        pqs = qs.filter(img_check=checked).distinct()
        print(pqs)
    elif car == 'all' and (not checked and checked != 'All'):
        print('in here', checked)
        pqs = qs
    

    
    objects = get_image_path(pqs)
    
    cars = show_cars()
    context = {
                'objects': objects,
                'car': car,
                'cars': cars,
                'checked': checked,

            }
    return render(request, 'admin/photo_listing.html', context)


def get_image_path_all(obj):
    working_dir = settings.STATICFILES_DIRS[1] 
    files  =  os.listdir(os.path.join(working_dir, obj.cat_n))
    img_list = []
    for f in files:
        try:
            img_list.append({ 'path': os.path.join(obj.cat_n, f), 'img_name': f})
        except Exception as e:
            print(e)
    setattr(obj, 'image_path', img_list ) 
    return obj


@login_required
def admin_detailed_view(request, pk):
    car = request.GET.get('car')
    checked = request.GET.get('checked')
    if car:
        request.session['car'] = car
    qs = Products.objects.get(id=pk)
    objects = get_image_path_all(qs)
    dir_listing = os.listdir(os.path.join(settings.STATICFILES_DIRS[1],qs.cat_n))    
    
    img_delete = request.GET.getlist('img_delete')
    if img_delete:
        for img_stay in img_delete:
            if img_stay in dir_listing:
                dir_listing.remove(img_stay)
        for f in dir_listing:
            os.remove(os.path.join(settings.STATICFILES_DIRS[1], qs.cat_n, f))
        return redirect('admin_detailed_view', pk)

    
    f = request.GET.get('delete_single')
    if f:
        os.remove(os.path.join(settings.STATICFILES_DIRS[1], qs.cat_n, f))
        return redirect('admin_detailed_view', pk)

    ready = request.GET.get('make_done')
    not_ready = request.GET.get('make_not_done')
    make_main = request.GET.get('make_main')
    par_id = qs.cat.first().parent_id
    if ready:
        qs.img_check=True
        qs.save()
        return redirect('adminphotolisting', par_id)
    if not_ready:
        qs.img_check=False
        qs.save()
        return redirect('admin_detailed_view', pk)
    if make_main:
        qs.main_img = make_main
        qs.save()
        return redirect('admin_detailed_view', pk)

    car = request.session['car']
    
    if request.session.get('car', None): 
        car = request.session['car']
        if request.GET.get('clear_session') == 'y':
            del request.session['car']
            return redirect('admin_detailed_view', pk)
    cars = show_cars()
        
    context = {
            'images': objects,
            'car': car,
            'cars': cars,
            'category_id': par_id,
            'checked': checked,
            }
    return render(request, 'admin/photo_detailed.html', context)


@login_required
def upload_files(request, pk):
    qs = Products.objects.get(id=pk)
    dir_path = os.path.join(settings.STATICFILES_DIRS[1], qs.cat_n)
    for count, x in enumerate(request.FILES.getlist("files")):
        ext = os.path.splitext(x.name)[-1]
        timestamp = timezone.now().timestamp()     
        file_name = str(qs.id) + '_100-' + str(timestamp) + ext 
        file_path = os.path.join(dir_path, file_name)  
        with open(file_path, 'wb+') as destination:
            for chunk in x.chunks():
                destination.write(chunk)
    return redirect('admin_detailed_view', qs.pk)



@login_required
def admin_photos_statistic(request):
    context = {

            }
    return render(request, 'admin/statistic.html', context)



@login_required
def create_dirs(request):

    working_dir = settings.STATICFILES_DIRS[1] 
    qs = Products.objects.all()
    i = 0
    for obj in qs:
        directory  =  os.path.join(working_dir, obj.cat_n)
        if not os.path.exists(directory):
            os.makedirs(directory)
            i += 1
    context = {
            'dirs_created': i,
            }
    return render(request, 'admin/make_dirs.html', context)

def set_session(var):
    var = str(var)
    if var:
        request.session[var] = var
        return True
    else:
        del request.session[var]
        return False
    


def admin_photo_search(request):
    search = request.GET.get('search')
    car = request.GET.get('car')
    checked = request.GET.get('checked')
        

    if search is not None:   # Поиск не пустой выбираем все по поиску
        print('search is not none only')
        qs = Products.objects.filter(Q(cat__name__icontains=search) | Q(cat_n__icontains=search) | Q(name__icontains=search)).distinct()
        
    if car == 'all' and checked == 'All':
        pqs = qs[:100]
    elif car != 'all' and checked != 'All':
        pqs = qs.filter(Q(cat__name__icontains=search) | Q(cat_n__icontains=search) | Q(name__icontains=search)).filter(car=car).filter(img_check=checked).distinct()[:100]
    elif car != 'all' and checked == 'All':
        pqs = qs.filter(Q(cat__name__icontains=search) | Q(cat_n__icontains=search) | Q(name__icontains=search)).filter(car=car).distinct()[:100]
    elif car == 'all' and checked != 'All':
        pqs = qs.filter(Q(cat__name__icontains=search) | Q(cat_n__icontains=search) | Q(name__icontains=search)).filter(img_check=checked).distinct()[:100]


        
    objects = get_image_path(pqs)
    
    cars = show_cars()
    context = {
                'objects': objects,
                'car': car,
                'cars': cars,
                'checked': checked,

            }
    return render(request, 'admin/photo_listing.html', context)
