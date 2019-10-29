from django.shortcuts import render, redirect
from .models import Kernel, Nomenklatura, Groups, CleanKernel, InfoKernel
import os
import csv
from functools import reduce
import operator
from .forms import KeyWordForm, UploadFileForm, CleanForm
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core import serializers
import json
from products.models import Categories
from django.db.models import Count
from django.contrib.auth.decorators import login_required


def kernel_clean(request):
    clean_form = CleanForm(request.POST)
    qs = Kernel.objects.all()[:100]
    if clean_form.is_valid():
        minus = clean_form.cleaned_data['minus'].split('\n')
        minus = [x.strip() for x in minus]
        ker_qs = Kernel.objects.exclude(reduce(operator.or_, (Q(keywords__icontains=x) for x in minus)))
        ker_qs_json = serializers.serialize('json', ker_qs)
        mun = '\n'.join(minus)
        if request.is_ajax():
            data = {
                    'keys': ker_qs_json,
                    }
            return JsonResponse(data, safe=False) 
        if request.POST.get('save') == 'clean':
            request.session['clean_mode'] = 'clean'
            ker, created = CleanKernel.objects.get_or_create(
                minus = mun
                )
            return redirect('dictionary:kernelclean')
        elif request.POST.get('save') == 'info':
            request.session['clean_mode'] = 'info'
            ker, created = InfoKernel.objects.get_or_create(
                minus = mun
                )
            return redirect('dictionary:kernelclean')
    context = {
            'clean_form': clean_form, 
            'kernel': qs,
            }
    return render(request, 'admin/dictionary/kernel_work.html', context)

def load_kernel(request):
    if request.GET.get('kernel_mode') == 'clean':
        qs = CleanKernel.objects.all()
    elif request.GET.get('kernel_mode') == 'info':
        qs = InfoKernel.objects.all()
    if request.is_ajax():
        minus = [x.minus for x in qs]
        data = '\n'.join(minus)
        data = {'minus': data}
        return JsonResponse(data, safe=False)







        

def handle_uploaded_file(f):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'files', f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def categorizer(request):

    context = {
            'some': 'context',
            }
    return render(request, 'admin/dictionary/categorizer.html', context)


@login_required
def insert_kernel(request, mode):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'files')
    ker = Kernel()
    nom = Nomenklatura()
    file_name = request.GET.get('filename')
    if file_name:
        pa = os.path.join(path, file_name)
    i = None
    j = None
    if request.GET.get('delete') and pa:
        os.remove(pa)
        return redirect('dictionary:insert_kernel', 'view')
    if mode == 'kernel':
        #i = ker.file_insert(pa)    
        return redirect('dictionary:insert_kernel', 'view')
    elif mode == 'nom':
        #j = nom.file_insert(pa)
        return redirect('dictionary:insert_kernel', 'view')
    context = {
            'inserted_ker': i,
            'inserted_nom': j,
            }
    if mode == 'view':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
        files = os.listdir(path)
        context = {
                'file_form': form,
                'files': files,
                }
            
        return render(request, 'admin/dictionary/insert.html', context)

@login_required
def change_group(request, pk):
    qs = Groups.objects.get(id=pk)
    plus = qs.plus.split('\n')
    plus = [x.strip() for x in plus]
    minus = qs.minus.split('\n')
    minus = [x.strip() for x in minus]
    ker_qs = Kernel.objects.filter(reduce(operator.or_, (Q(keywords__icontains=x) for x in
        plus))).exclude(reduce(operator.or_, (Q(keywords__icontains=x) for x in minus)))
    nom_qs = Nomenklatura.objects.filter(reduce(operator.or_, (Q(name__icontains=x) for x in
        plus))).exclude(reduce(operator.or_, (Q(name__icontains=x) for x in minus)))
    ker_qs_json = serializers.serialize('json', ker_qs)
    nom_qs_json = serializers.serialize('json', nom_qs)
    key_form = KeyWordForm(request.GET)
    context = {
            'kernels': ker_qs,
            'Nomenklatura': nom_qs,
            'key_form': key_form,
            }

    return render(request, 'admin/dictionary/listing.html', context)



@login_required
def main_work(request):
    ker_qs = Kernel.objects.all().exclude(chk=True).order_by('?')[:100]
    nom_qs = Nomenklatura.objects.all().exclude(chk=True).order_by('?')[:100]
    group_qs = Groups.objects.all().order_by('name')
    key_form = KeyWordForm(request.GET)
    if key_form.is_valid():
        parent = key_form.cleaned_data['parent']
        plus = key_form.cleaned_data['plus'].split('\n')
        plus = [x.strip() for x in plus]
        minus = key_form.cleaned_data['minus'].split('\n')
        minus = [x.strip() for x in minus]
        group_name = key_form.cleaned_data['group_name']
        ker_qs = Kernel.objects.filter(reduce(operator.or_, (Q(keywords__icontains=x) for x in
            plus))).exclude(reduce(operator.or_, (Q(keywords__icontains=x) for x in minus))).exclude(chk=True)
        nom_qs = Nomenklatura.objects.filter(reduce(operator.or_, (Q(name__icontains=x) for x in
            plus))).exclude(reduce(operator.or_, (Q(name__icontains=x) for x in minus))).exclude(chk=True)
        ker_qs_json = serializers.serialize('json', ker_qs)
        nom_qs_json = serializers.serialize('json', nom_qs)
        
        if request.is_ajax():
            data = {
                    'keys': ker_qs_json,
                    'noms': nom_qs_json,
                    }
            return JsonResponse(data, safe=False) 
        if request.GET.get('save_group'):
            group, created = Groups.objects.update_or_create(
                    name = group_name,
                    defaults={
                            'plus':  '\n'.join(plus),
                            'minus': '\n'.join(minus),
                            'parent_id' : parent.id,
                    }
                    )
            ker_qs.update(chk=True)
            nom_qs.update(chk=True)
            return redirect('dictionary:main_work')

    #Aggregate statistics
    group_count = Groups.objects.count()
    ker_count = Kernel.objects.filter(chk=True).count()
    ker_count_tot = Kernel.objects.count()
    nom_count = Nomenklatura.objects.filter(chk=True).count()
    nom_count_tot = Nomenklatura.objects.count()
    counts = {'gk': group_count, 'kk': ker_count, 'nk': nom_count, 'kk_tot': ker_count_tot, 'nk_tot': nom_count_tot}
    
    context = {
            'kernels': ker_qs,
            'nomenklatura': nom_qs,
            'groups': group_qs,
            'key_form': key_form,
            'counts': counts,
            }
    return render(request, 'admin/dictionary/listing.html', context)


@login_required
def check_group(request):
    group_name = request.GET.get('group_data')
    chk = Groups.objects.get(name=group_name)
    if chk:
        data = {
                'group_name': chk.name,
                'plus': chk.plus,
                'minus':chk.minus,
                'parent_cat': chk.parent_id,
                }
        return JsonResponse(data)

@login_required
def view_group(request, pk):
    group = Groups.objects.get(id=pk)
    plus = group.plus.split('\n')
    plus = [x.strip() for x in plus]
    minus = group.minus.split('\n')
    minus = [x.strip() for x in minus]
    ker_qs = Kernel.objects.filter(reduce(operator.or_, (Q(keywords__icontains=x) for x in
        plus))).exclude(reduce(operator.or_, (Q(keywords__icontains=x) for x in minus)))
    nom_qs = Nomenklatura.objects.filter(reduce(operator.or_, (Q(name__icontains=x) for x in
        plus))).exclude(reduce(operator.or_, (Q(name__icontains=x) for x in minus)))
    context = {
            'group': group,
            'plus': plus,
            'minus': minus,
            'ker': ker_qs,
            'nom': nom_qs,
            }
    return render(request, 'admin/dictionary/group_view.html', context)

@login_required
def view_groups(request):
    groups = Groups.objects.all()
    def chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i+n]
    gl = [x for x in chunks(groups, 100)]
    context = {
            'groups': gl,
            'count': groups.count(),
            }
    return render(request, 'admin/dictionary/groups_view.html', context)
