from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Products, Categories, Cart, CartItem
from django.db.models import Count, Min, Max
from django.db.models import Q, Subquery
from django.conf import settings
import os
from django.core.mail import send_mail



def cart_view(request):

    cart_id = request.session.get('cart_id')
    cart = Cart.objects.get(id=cart_id)
    request.session['total'] = cart.items.count()

    print(cart.id ,cart.items.count())
    context = {
            'cart': cart,
            }
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, product_id):

    product = Products.objects.get(id=product_id)
    new_item, created = CartItem.objects.get_or_create(product=product, item_total=product.price)
    if request.session.get('cart_id'):
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    else:
        
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)


    if new_item not in cart.items.all():
        cart.items.add(new_item)
        cart.save()
        return HttpResponseRedirect('/cart/')

def remove_from_cart(request, product_id):

    if request.session.get('cart_id'):
        cart_id = request.session.get('cart_id')
        cart = Cart.objects.get(id=cart_id)
        for cart_item in cart.items.all():
            if cart_item.product.id == product_id:
                cart.items.remove(cart_item)
                cart.save()
                request.session['total'] = cart.items.count()
                return HttpResponseRedirect('/cart/')
            else:
                return HttpResponseRedirect('/cart/')
