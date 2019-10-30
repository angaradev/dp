from django.shortcuts import render, redirect
from .models import Kernel, Nomenklatura, Groups, CleanKernel, InfoKernel, KernelTmp
import os
import csv
from functools import reduce
import operator
from .forms import KeyWordForm, UploadFileForm, CleanForm, CategorizeKernel
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import json
from products.models import Categories
from django.db.models import Count
from django.contrib.auth.decorators import login_required
import itertools
from django.db import connection
from django.urls import reverse


@login_required
def insert_data(request):
    cursor = connection.cursor()
    table_name = 'group_dict_kerneltmp'
    q = 'TRUNCATE TABLE ' + table_name
    cursor.execute(q)
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'files')
    file_name = request.GET.get('filename')
    fil = os.path.join(path, file_name)
    with open(fil) as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        delimiter = dialect.delimiter
    statement = "LOAD DATA LOCAL INFILE %s INTO TABLE group_dict_kerneltmp FIELDS TERMINATED BY %s  (keywords, freq,@dummy2);"
    state = cursor.execute(statement, [fil, delimiter])
    context = {
            'insert_count': state,
            }
    if context:
        return redirect(reverse('dictionary:categorizer'))
    else:
        return render(request, 'admin/dictionary/categorizer.html', context)

@login_required
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


@login_required
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

@login_required
def categorizer(request):
    def q_plus(kernel, plus):
        for rec in kernel:
            matches = {s for s in kernel if any(w in s for w in plus)}
        return(matches)

    def q_minus(plus_set, minus):
        for rec in plus_set:
            non_matches = {s for s in plus_set if not any(w in s for w in minus)}
        return non_matches

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'files')
    files = os.listdir(path)
    file_name = request.GET.get('filename')
    sample = []
    cat_count = 0
    not_cat_count = 0
    final_set = set()
    if request.GET.get('mode') == 'preview' and file_name:
        pa = os.path.join(path, file_name)
        with open(pa, 'r') as f_csv:
            reader = csv.reader(f_csv, delimiter=';')
            for i,line in enumerate(reader):
                sample.append(line)
                if i == 10:
                    break
    elif request.GET.get('mode') == 'categorize' and file_name:
        pa = os.path.join(path, file_name)
        dic = Groups.objects.all()

        for drow in dic:        
            plus = drow.plus.split('\n')
            plus = [x.strip() for x in plus]
            minus = drow.minus.split('\n')
            minus = [x.strip() for x in minus]
            ker_qs = KernelTmp.objects.filter(reduce(operator.or_, (Q(keywords__icontains=x) for x in
            plus))).exclude(reduce(operator.or_, (Q(keywords__icontains=x) for x in minus))).exclude(chk=True)
            ker_qs.update(group_id=drow.id)
            print(plus, minus)
            print(ker_qs)
        final_qs = KernelTmp.objects.all()
        cat_count = final_qs.filter(~Q(group_id=0)).count()
        not_cat_count = final_qs.filter(group_id=0).count()

        
    context = {
            'files': files,
            'sample': sample,
            'cat_count': cat_count,
            'not_cat_count': not_cat_count,
            }
    return render(request, 'admin/dictionary/categorizer.html', context)

def get_csv(request):
    resp = HttpResponse(content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="ready_kernel.csv"'
    writer = csv.writer(resp)
    qs = KernelTmp.objects.all()
    for row in qs:
        writer.writerow([row.keywords, row.freq, row.group_id])
    return resp

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
