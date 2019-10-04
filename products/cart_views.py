from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from .models import Products, Categories, Cart, CartItem, Orders
from django.db.models import Count, Min, Max
from django.db.models import Q, Subquery
from django.conf import settings
import os
from django.core.mail import send_mail, EmailMessage
from decimal import Decimal
from django.contrib.auth.models import User
from .forms import OrderForm
from django.template.loader import render_to_string




def order_success(request, order_n):
    context = {
            'order_n': order_n,
            }
    return render(request, 'cart/success.html', context)


def order_view(request):
    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
    else:
        cart = None
    action = request.POST.get('action', None)
    order = None
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        user_id = request.user.id
        email   = user.email
        address = user.profile.address
        phone   = user.profile.phone
        initial_data = {
                'email': email,
                'address': address,
                'phone': phone,
                }
        print(initial_data)        
                
                
    else:
        initial_data = None
        user = None
        user_id = None
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        address = request.POST.get('address', None)
    
    # Определяю функцию для отправки писем заказа
    def send_html_email_customer(order):
        subject = 'Заказ запчастей на DucatoParts'
        sender = settings.SHOP_EMAIL_FROM
        receiver = email
        shop_address = [settings.SHOP_ADDRESS_LINE_1, settings.SHOP_ADDRESS_LINE_2]
        context = { 'cart': cart, 'order': order }
        html_msg = render_to_string('cart/order_email.html', context)  
        msg = EmailMessage(subject=subject, body=html_msg, from_email=sender, bcc=(receiver,))
        msg.content_subtype = 'html'
        return msg.send()

    order_form = OrderForm(request.POST or None, initial=initial_data)
    if request.session['cart_id']:
        comments = request.POST.get('comments', None)
        if action == 'order':
            if order_form.is_valid():
                instance = order_form.save(commit=False)
                instance.cart = cart
                instance.save()
                order_n = Orders.objects.get(cart=cart)
                if email:
                    send_html_email_customer(order_n)
                del request.session['cart_id']
                del request.session['total']
                return redirect('order_success', order_n.order_n)
                




        
    context = {
            'cart': cart,
            'order_form': order_form,
            'order_user': user,
            }
    return render(request, 'cart/checkout.html', context)


def cart_view(request):

    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    else:
        cart = None
        if request.session.get('total'):
            del request.session['total'] 

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














