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
    qs = Products.objects.get(id=pk)
    objects = get_image_path_all(qs)
    dir_listing = os.listdir(os.path.join(settings.STATICFILES_DIRS[1],qs.cat_n))    
    print(dir_listing)
    img_delete = request.GET.getlist('img_delete')
    if img_delete:
        for f in img_delete:
            os.remove(os.path.join(settings.STATICFILES_DIRS[1], f))
        return redirect('admin_detailed_view', pk)
    context = {
            'images': objects,
            }
    return render(request, 'admin/photo_detailed.html', context)



class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'upload.html'  # Replace with your template.
    success_url = '...'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                ...  # Do something with each file.
            return self.form_valid(form)
        else:
            return self.form_invalid(form)











    
