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
from .forms import OrderForm, PaymentForm
from django.template.loader import render_to_string




def order_success(request, order_n):
    try:
        del request.session['cart_id']
        del request.session['total']
        
        context = {
                'order_n': order_n,
                }
        return render(request, 'cart/success.html', context)
    except:
        return redirect('home')


def order_view(request):
    cart_id = request.session.get('cart_id', None)
    cart = None
    if cart_id:
        cart = Cart.objects.get(id=cart_id)

    action = request.POST.get('action', None)
    payment_online = request.POST.get('payment_online', None)

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
    else:
        initial_data = None
        user = None
        user_id = None
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        request.session['tel'] = phone
        address = request.POST.get('address', None)
    
    # Определяю функцию для отправки писем заказа
    def send_html_email(order, receiver, template, t='manager'):
        if request.user.is_authenticated:
            phone = request.user.profile.phone
        elif order.phone is not None:
            phone = order.phone
        else:
            phone = None
        email = None
        if request.user.is_authenticated:
            email = request.user.email
        elif order.email is not None:
            email = order.email
        address = None
        if request.user.is_authenticated:
            address = request.user.profile.address
        elif order.address is not None:
            address = order.address
        subject = 'Заказ запчастей на DucatoParts'
        sender = settings.SHOP_EMAIL_FROM
        shop_address = [settings.SHOP_ADDRESS_LINE_1, settings.SHOP_ADDRESS_LINE_2]
        context = { 'cart': cart, 'order': order, 'phone': phone, 'email': email, 'address': address }
        html_msg = render_to_string(template, context)  
        if not isinstance(receiver, list):
            receiver = [receiver,]
        msg = EmailMessage(subject=subject, body=html_msg, from_email=sender, bcc=receiver)
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
                request.session['order_n'] = order_n.order_n
                send_html_email(order_n, settings.SHOP_EMAILS_MANAGERS, 'cart/order_email_manager.html')
                print(settings.SHOP_EMAILS_MANAGERS)
                if email:
                    send_html_email(order_n, email, 'cart/order_email.html')
                if payment_online == 'True':
                    return redirect('paymentmethod')

                else:
                    return redirect('order_success', order_n.order_n)
        
    context = {
            'cart': cart,
            'order_form': order_form,
            'order_user': user,
            }
    return render(request, 'cart/checkout.html', context)



def payment_method(request):
   
    cart = Cart.objects.get(id=request.session.get('cart_id'))
    if request.user.is_authenticated:
        initial_data = {
                'sum': cart.cart_total,
                'customerNumber': request.user.profile.phone,
                }
    elif request.session.get('tel'):
        initial_data = {
                'sum': cart.cart_total,
                'customerNumber': request.session.get('tel')
                }
    else:

        initial_data = {
                'sum': cart.cart_total,
                }
    payment_form = PaymentForm(request.POST or None, initial=initial_data)
    order_n = request.session.get('order_n') 
    context = {
            'order_n': order_n,
            'payment_form': payment_form,
            'cart_total': request.session['total'],
            'cart_id': request.session['cart_id'],
            }
    del request.session['cart_id']
    del request.session['total']
    return render(request, 'cart/payment.html', context)








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
    product_id = request.GET.get('product_id', None)

    if product_id is not None:
        product = Products.objects.get(id=product_id)
        new_item, created = CartItem.objects.get_or_create(product=product, item_total=product.price)

        if request.session.get('cart_id', None):
            cart_id = request.session['cart_id']
            cart = Cart.objects.get(id=cart_id)
            request.session['total'] = cart.items.count()
        else:
            cart = Cart()
            #cart.save()
            cart_id = cart.id
            request.session['cart_id'] = cart_id
            #cart = Cart.objects.get(id=cart_id)
        
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
            try:
                return JsonResponse(json_data)
            except Exception as e:
                print(e)


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Wishlist logic
def add_to_wish(request):
    product_id = request.GET.get('product_id', None)
    if product_id:
        if not 'wish_list' in request.session or not request.session['wish_list']:
            request.session['wish_list'] = [product_id]
        else:
            wish_list = request.session['wish_list']
            if product_id not in wish_list:
                wish_list.append(product_id)
            request.session['wish_list'] = wish_list
        if request.session.get('wish_list'):
            json_data = {
                    'wish_list': request.session['wish_list'],
                    'wish_list_count': len(request.session.get('wish_list'))
                    }
        else:
            json_data = {
                    'wish_list': request.session.get('wish_list', None)
                    }
    return JsonResponse(json_data)

def see_wish(request):
    wish_list = request.session.get('wish_list', None)
    objects = None
    if wish_list:
        objects = Products.objects.filter(id__in=wish_list)
    context = {
            'objects': objects,
            }
    return render(request, 'cart/wishlist.html', context)
    
def remove_wish(request):
    wish_list = None
    product_id = request.GET.get('product_id', None)
    if product_id:
        wish_list = request.session['wish_list']
        if product_id in wish_list:
            wish_list.remove(product_id)
            request.session['wish_list'] = wish_list
        if request.is_ajax:
            json_data = {
                    'wish_list': wish_list,
                    'wish_list_count': len(wish_list),
                    } 
            return JsonResponse(json_data)
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
def clear_wish(request):
    del request.session['wish_list']
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

        if request.is_ajax:
            json_data = {
                    'cartItemCount': cart.items.count(),
                    'cart_total': new_cart_total,
                    }
            request.session['total'] = cart.items.count()
            return JsonResponse(json_data)
        else:
            return redirect(request.META.get('HTTP_REFFERER'))
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














