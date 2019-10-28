from django.shortcuts import render, redirect
from .models import Kernel, Nomenklatura, Groups
import os
import csv
from functools import reduce
import operator
from .forms import KeyWordForm
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core import serializers
import json
from products.models import Categories

def insert_kernel(request):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'files/kernel2.csv')
    path2 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'files/parts1.csv')
    ker = Kernel()
    nom = Nomenklatura()
    i = ker.file_insert(path)    
    j = nom.file_insert(path2)
    context = {
            'inserted_ker': i,
            'inserted_nom': j,
            }
    return render(request, 'admin/dictionary/insert.html', context)


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
                            'parent_id' : parent,
                    }
                    )
            ker_qs.update(chk=True)
            nom_qs.update(chk=True)
            return redirect('dictionary:main_work')
    context = {
            'kernels': ker_qs,
            'nomenklatura': nom_qs,
            'groups': group_qs,
            'key_form': key_form,
            }
    return render(request, 'admin/dictionary/listing.html', context)


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





def main_work_back(request):
     
    pl = request.GET.get('plus').split('\n')
    pl = [x.strip() for x in pl]
    mi = request.GET.get('minus').split('\n')
    mi = [x.strip() for x in mi]
    ker_qs = Kernel.objects.filter(reduce(operator.or_, (Q(keywords__icontains=x) for x in
            pl))).exclude(reduce(operator.or_, (Q(keywords__icontains=x) for x in mi))).order_by('keywords')
    nom_qs = Nomenklatura.objects.filter(reduce(operator.or_, (Q(name__icontains=x) for x in
            pl))).exclude(reduce(operator.or_, (Q(name__icontains=x) for x in mi))).order_by('name')
    group_qs = Groups.objects.all()
    key_form = KeyWordForm(request.GET)
    if key_form.is_valid():
        plus = key_form.cleaned_data['plus'].split('\n')
        plus = [x.strip() for x in plus]
        minus = key_form.cleaned_data['minus'].split('\n')
        minus = [x.strip() for x in minus]

        ker_qs = ker_qs.filter(reduce(operator.or_, (Q(keywords__icontains=x) for x in
            plus))).exclude(reduce(operator.or_, (Q(keywords__icontains=x) for x in minus)))
        nom_qs = nom_qs.filter(reduce(operator.or_, (Q(name__icontains=x) for x in
            plus))).exclude(reduce(operator.or_, (Q(name__icontains=x) for x in minus)))
        ker_qs_json = serializers.serialize('json', ker_qs)
        nom_qs_json = serializers.serialize('json', nom_qs)
        if request.is_ajax():
            data = {
                    'keys': ker_qs_json,
                    'noms': nom_qs_json,
                    }
            return JsonResponse(data, safe=False) 
        if requset.GET.get('save'):
            print('save in request')
    context = {
            'kernels': ker_qs,
            'nomenklatura': nom_qs,
            'groups': group_qs,
            'key_form': key_form,
            }
    return render(request, 'admin/dictionary/listing.html', context)
