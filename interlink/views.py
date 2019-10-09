from django.shortcuts import render, redirect
from .models import Tableredirectcat
from products.models import Categories
from django.http import HttpResponsePermanentRedirect

def subcat_redirect(request, pk):
    qs = Tableredirectcat.objects.get(id_old=pk)
    nqs = Categories.objects.get(id=qs.id_new)
    return redirect('subcat', nqs.slug) 
