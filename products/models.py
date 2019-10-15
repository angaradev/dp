# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.urls.base import reverse
from django.utils import timezone
from django.conf import settings
import os
from django.db.models.signals import pre_save
from .utils import random_string_generator
from urllib.parse import quote

class Categories(models.Model):
    name = models.CharField(max_length=100, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.CharField(max_length=500, blank=True, null=True)


    class Meta:
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('subcat', kwargs={'slug': self.slug })


class Cross(models.Model):
    orig_n = models.CharField(max_length=50)
    oem_n = models.CharField(max_length=50)


class Products(models.Model):
    cat = models.ManyToManyField('Categories', blank=True, related_name='cat')
    name = models.CharField(max_length=255, null=True)
    cat_n = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=100, null=True)
    car = models.CharField(max_length=255, null=True)
    car_model = models.CharField(max_length=255, null=True)
    cross = models.ManyToManyField(Cross, verbose_name="cross verbose name")
    price = models.FloatField(null=True, blank=True)
    cond = models.BooleanField(default=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    real_weight = models.FloatField(blank=True, null=True)
    seller = models.CharField(max_length=100, blank=True, null=True)
    main_img = models.CharField(max_length=500, blank=True, null=True)
    img_check = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    
    def get_absolute_url(self):
       return reverse('detailed', kwargs={'pk': self.id})


    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        qs = ContentType.objects.get_for_model(instance.__class__)
        return qs

    @property
    def image_path(self):
        working_dir = settings.STATICFILES_DIRS[1]
        if self.main_img:
            f = os.path.join(self.cat_n, self.main_img)
            if not os.path.isfile(f):
                files = os.listdir(os.path.join(working_dir, self.cat_n))
                try:
                    f = os.path.join(self.cat_n, files[0])
                except:
                    f = '000_default/default.png'

        else:
            try:
                files = os.listdir(os.path.join(working_dir, self.cat_n))
                f = os.path.join(self.cat_n, files[0])
            except Exception as e:
                f = '000_default/default.png'
        return f

    @property
    def image_path_all(self):
            working_dir = settings.STATICFILES_DIRS[1] 
            files  =  os.listdir(os.path.join(working_dir, self.cat_n))[:15]
            print(files)
            img_list = []
            for f in files:
                img_list.append(os.path.join(self.cat_n, f))
            if not img_list:
                f = ['000_default/default.png' for _ in range(5)]
            else:
                f = img_list
            return f







class CartItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE )
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return 'Cart item for product {}'.format(self.product.name)

class Cart(models.Model):

    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    timestamp = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Orders(models.Model):

    user_bound  = models.PositiveIntegerField(blank=True, null=True)
    email       = models.EmailField(max_length=200, blank=True, null=True)
    phone       = models.CharField(max_length=20)
    address     = models.CharField(max_length=500, blank=True, null=True)
    created     = models.DateField(auto_now_add=True)
    cart        = models.OneToOneField(Cart, on_delete=models.CASCADE, default=1)
    comments    = models.CharField(max_length=500, blank=True, null=True)
    order_n     = models.CharField(max_length=50, blank=True, null=True) 

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.phone


def create_order_n(sender, instance, *args, **kwargs):
    instance.order_n = random_string_generator(4)

pre_save.connect(create_order_n, sender=Orders)










