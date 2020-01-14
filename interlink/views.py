from django.shortcuts import render, redirect
from .models import RedireCtcat, RedirectProductOldToNew, RedirectProductOldToNewDictionary
from products.models import Categories
from django.http import Http404

def subcat_redirect(request, pk):
    try:
        qs = RedireCtcat.objects.filter(id_old=pk).first()
        nqs = Categories.objects.get(id=qs.id_new)
        return redirect('subcat', nqs.slug, permanent=True) 
    except:
        raise Http404


def subcat_ducato_redirect(request, pk):
    try:
        qs = RedireCtcat.objects.filter(id_old=pk).first()
        nqs = Categories.objects.get(id=qs.id_new)
        return redirect('car_page_subcats', 'fiat-ducato', nqs.slug, permanent=True) 
    except:
        raise Http404


def subcat_boxer_redirect(request, pk):
    try:
        qs = RedireCtcat.objects.filter(id_old=pk).first()
        nqs = Categories.objects.get(id=qs.id_new)
        return redirect('car_page_subcats', 'peugeot-boxer', nqs.slug, permanent=True) 
    except:
        raise Http404


def subcat_jumper_redirect(request, pk):
    try:
        qs = RedireCtcat.objects.filter(id_old=pk).first()
        nqs = Categories.objects.get(id=qs.id_new)
        return redirect('car_page_subcats', 'peugeot-boxer', nqs.slug, permanent=True) 
    except:
        raise Http404

def analog_part_brand(request, old_url):
    try:
        qs = RedirectProductOldToNew.objects.filter(url=old_url).first()
    except:
        cat_qs = RedirectProductOldToNewDictionary.objects.filter(url=old_url).first()
        if not cat_qs:
            raise Http404
        # Это костыль для категорий которых нет у нас но есть в словаре
        if cat_qs.id_new == 0 or cat_qs.id_new > 2504:
            return redirect('newparts', permanent=True)
        cat = Categories.objects.get(id=cat_qs.id_new)
        return redirect('subcat', cat.slug, permanent=True) 
        if not cat_qs:
            raise Http404()
    return redirect('detailed', qs.id_new, permanent=True) 





