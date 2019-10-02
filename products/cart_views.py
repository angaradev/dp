from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .models import Products, Categories, Cart, CartItem
from django.db.models import Count, Min, Max
from django.db.models import Q, Subquery
from django.conf import settings
import os
from django.core.mail import send_mail
from decimal import Decimal



def cart_view(request):

    cart_id = request.session.get('cart_id')
    cart = Cart.objects.get(id=cart_id)
    request.session['total'] = cart.items.count()

    context = {
            'cart': cart,
            }
    return render(request, 'cart/cart.html', context)


def add_to_cart(request):

    product_id = request.GET.get('product_id')

    if product_id is not None:
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

        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save()


        if request.is_ajax():
            json_data = {
                    'cartItemCount': cart.items.count(),
                    'cart_total': new_cart_total,
                    }
            request.session['total'] = cart.items.count()
            return JsonResponse(json_data)
            

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def remove_from_cart(request):


    product_id = int(request.GET.get('product_id'))

    if request.session.get('cart_id'):
        cart_id = int(request.session.get('cart_id'))
        cart = Cart.objects.get(id=cart_id)
        for cart_item in cart.items.all():
            if cart_item.product.id == int(product_id):
                cart.items.remove(cart_item)
                cart.save()
                request.session['total'] = cart.items.count()
        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save()

        if request.is_ajax():
            json_data = {
                    'cartItemCount': cart.items.count(),
                    'cart_total': new_cart_total,
                    }
            request.session['total'] = cart.items.count()
            return JsonResponse(json_data)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def update_cart(request):
    if request.session.get('cart_id'):
        cart_id = int(request.session.get('cart_id'))
        cart = Cart.objects.get(id=cart_id)

    quantity = int(request.GET.get('quantity'))
    item_id = int(request.GET.get('item_id'))
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.quantity = quantity
    cart_item.item_total = Decimal(cart_item.product.price * quantity)
    cart_item.save()
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()

    context = {
            'cartItemCount': cart.items.count(),
            'item_total': cart_item.item_total,
            'cart_total': new_cart_total,
            }
    return JsonResponse(context)

def clear_cart(request):
    if request.session.get('cart_id'):
        cart_id = int(request.session.get('cart_id'))
        cart = Cart.objects.get(id=cart_id)
        for item in cart.items.all():
            cart.items.remove(item)
        return HttpResponseRedirect('cart')














