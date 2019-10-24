from products.models import Cart, Products, Categories
from django.conf import settings

def small_cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        try:
            context = {'cart': Cart.objects.get(id=cart_id)}
            return context
        except:
            return {'cart': None}
    else:
        return {'cart': None}

# Вывод контактной информации

def contact_info(request):
    return({'shop_info': settings.SHOP_CONTACT_INFO, 'site_host': settings.SHOP_SITE_HOST})


def sales_products(request):
    cats = Categories.objects.filter(parent_id=0)
    prod_list = settings.SALES_ON_SEARCH
    products = Products.objects.filter(id__in=prod_list)
    context = {
            'brakes': products,
            'categories': cats,
            }
    return(context)

