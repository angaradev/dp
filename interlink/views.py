from django.shortcuts import render, redirect
from .models import RedireCtcat, RedirectProductOldToNew, RedirectProductOldToNewDictionary
from products.models import Categories
from django.http import Http404

def subcat_redirect(request, pk):
    qs = RedireCtcat.objects.get(id_old=pk)
    print(qs)
    nqs = Categories.objects.get(id=qs.id_new)
    if not qs or not nqs:
        raise Http404
    return redirect('subcat', nqs.slug, permanent=True) 


def subcat_ducato_redirect(request, pk):
    qs = RedireCtcat.objects.get(id_old=pk)
    nqs = Categories.objects.get(id=qs.id_new)
    if not qs or not nqs:
        raise Http404
    return redirect('car_page_subcats', 'fiat-ducato', nqs.slug, permanent=True) 


def subcat_boxer_redirect(request, pk):
    qs = RedireCtcat.objects.get(id_old=pk)
    nqs = Categories.objects.get(id=qs.id_new)
    if not qs or not nqs:
        raise Http404
    return redirect('car_page_subcats', 'peugeot-boxer', nqs.slug, permanent=True) 


def subcat_jumper_redirect(request, pk):
    qs = RedireCtcat.objects.get(id_old=pk)
    nqs = Categories.objects.get(id=qs.id_new)
    if not qs or not nqs:
        raise Http404
    return redirect('car_page_subcats', 'peugeot-boxer', nqs.slug, permanent=True) 

def analog_part_brand(request, old_url):
    qs = RedirectProductOldToNew.objects.filter(url=old_url).first()
    if not qs:
        cat_qs = RedirectProductOldToNewDictionary.objects.filter(url=old_url).first()
        # Это костыль для категорий которых нет у нас но есть в словаре
        if cat_qs.id_new == 0 or cat_qs.id_new > 2504:
            return redirect('newparts', permanent=True)
        cat = Categories.objects.get(id=cat_qs.id_new)
        return redirect('subcat', cat.slug, permanent=True) 
        if not cat_qs:
            raise Http404()
    return redirect('detailed', qs.id_new, permanent=True) 





