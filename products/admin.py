from django.contrib import admin
from .models import Products, Cart, CartItem, Orders

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Orders)
