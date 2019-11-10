from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from .models import Products, Categories
from django.db.models import Count, Min, Max
from django.db.models import Q, Subquery
from django.core.paginator import Paginator
from django.conf import settings
import os
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from comments.models import Comment
from django.utils.html import strip_tags
from django.core.mail import send_mail
from email_form.forms import EmailFormLight, EmailFormOneField
from email_form.models import EmailModel
from star_ratings.models import Rating
from .utils import get_weight, search_splitter
from blogs.models import Blogs


def show_cars():
    qs = Products.objects.values('car').annotate(dcount=Count('car'))
    return qs

def show_brands(pk, car, cat):
    for k, v in kwargs.items():
        pass
    qs = Products.objects.filter(cat=cat).values('brand').annotate(dbrand=Count('brand'))
    return qs

def show_price(price_min, price_max):
    price_range = Products.objects.filter(price__range=[price_min, price_max])
    p_min = Products.objects.all().aggregate(Min('price'))
    p_max = Products.objects.all().aggregate(Max('price'))
    return p_min, p_max, price_range

def categories_tree(pk):

    if pk > 999:
        cats = Categories.objects.filter(id=pk)
    if pk < 999 and pk > 99:
        cats = Categories.objects.filter(parent_id=pk)
    if pk < 99:
        cats_sub = Categories.objects.filter(parent_id=pk)
        c_l = []
        for cat_sub in cats_sub:
            c_l.append(cat_sub.id)
        cats = Categories.objects.filter(parent_id__in=c_l)
    return cats        
    
def pag_def(show):
    if show == '40':
        return 40
    elif show == '60':
        return 60
    elif show == 'all':
        return 200
    else:
        return 20

def newparts(request):
    sort = request.GET.get('sort', None)
    show = request.GET.get('show', None)
    if sort == '2':
        qs = Products.objects.all().order_by('price')[:200]
    elif sort == '3':
        qs = Products.objects.all().order_by('-price')[:200]
    else:
        qs = Products.objects.all()[:200]

    pag = pag_def(show)
    cats = Categories.objects.filter(parent_id=0)
    try:
        p = Paginator(qs, pag)
        page = request.GET.get('page')
        objects = p.get_page(page)
    except:
        pass
    if request.GET.get('load_all') == 'all':
        objects = objects

    context = {
            'objects': objects, 
            'categories': cats,
            'cars': show_cars(),
            }
    return render(request, 'products/newparts.html', context)


def cars(request, car):
    sort = request.GET.get('sort', None)
    show = request.GET.get('show', None)
    if sort == '3':
        qs = Products.objects.filter(car=car).order_by('-price')[:200]
    elif sort == '2':
        qs = Products.objects.filter(car=car).order_by('price')[:200]
    else: 
        qs = Products.objects.filter(car=car).order_by('?')[:200]
    pag = pag_def(show)
    cats_tmp = Categories.objects.filter(parent_id=0)
    cats = []
    for c in cats_tmp:
        nums = Products.objects.filter(car=car, cat__in=categories_tree(c.id)).count()
        if nums != 0:
            setattr(c, 'prod_count', nums)
            cats.append(c)
    try:
        p = Paginator(qs, pag)
        page = request.GET.get('page')
        objects = p.get_page(page)
    except:
        pass
    if request.GET.get('load_all') == 'all':
        objects = qs

    context = {
            'objects': objects,
            'cars': show_cars(),
            'categories': cats,
            'car': car,
            }
    return render(request, 'products/newparts.html', context)

def cars_subcats(request, car, slug, **kwargs):
    brand = request.GET.get('brand', None)
    cats_tmp = Categories.objects.get(slug=slug)
    second_level_cats = Categories.objects.filter(parent_id=cats_tmp.id)
    cats = []
    for c in second_level_cats:
        nums = Products.objects.filter(car=car, cat__in=categories_tree(c.id)).count()
        if nums != 0:
            setattr(c, 'prod_count', nums) 
            cats.append(c)

    cats_list = [] 
    if len(cats) == 0:
        if brand:
            qs = Products.objects.filter(car=car, cat=cats_tmp.id, brand=brand).distinct()
        else:
            qs = Products.objects.filter(car=car, cat=cats_tmp.id).distinct()
    else:
        for c in cats:
            cats_list.append(c.id)
        groups = Categories.objects.filter(parent_id__in=cats_list)
        for g in groups:
            cats_list.append(g.id) 
        if brand:
            qs = Products.objects.filter(car=car, cat__in=cats_list, brand=brand).distinct()
        else:
            qs = Products.objects.filter(car=car, cat__in=cats_list).distinct()
    
    sort = request.GET.get('sort', None)
    show = request.GET.get('show', None)
    if sort == '2':
        qs = qs.order_by('price')
    elif sort == '3':
        qs = qs.order_by('-price')
    else:
        qs = qs 
    if not qs:
        raise Http404

    pag = pag_def(show)
    brands = qs.values('brand').annotate(brand_count=Count('brand')) 
    h1 = cats_tmp.name
    try:
        p = Paginator(qs, pag)
        page = request.GET.get('page')
        objects = p.get_page(page)
    except:
        pass
    if request.GET.get('load_all') == 'all':
        objects = qs



    #Article founder starts here
    search_list = search_splitter(h1)
    articles = Blogs.objects.all()
    art_w_list = []
    for i, article in enumerate(articles):
        we = get_weight(article.text, search_list)
        if we > 0.02:
            art_w_list.append({ 'article': article, 'weight': we})
        if i > 10:
            break
    

    context = {
            'objects': objects,
            'cars': show_cars(),
            'categories': cats,
            'car': car,
            'brands': brands,
            'title_h1': h1,
            'car': car,
            'brand': brand,
            'cat': cats_tmp,
            'articles': art_w_list,
            }
    
    return render(request, 'products/newparts.html', context)

# HERE IS SAME STUFF BUT NO CAR

def subcat(request, slug, **kwargs):
    brand = request.GET.get('brand', None)
    cats_tmp = Categories.objects.get(slug=slug)
    second_level_cats = Categories.objects.filter(parent_id=cats_tmp.id)



    if cats_tmp.id < 99:
        bread1 = Categories.objects.get(slug=slug, parent_id=0)
        bread2 = None
        bread3 = None
    elif cats_tmp.id > 99 and cats_tmp.id < 999:
        bread2 = cats_tmp
        bread1 = Categories.objects.get(id=bread2.parent_id)
        bread3 = None
    else:
        bread3 = cats_tmp
        bread2 = Categories.objects.get(id=bread3.parent_id)
        bread1 = Categories.objects.get(id=bread2.parent_id)


    cats = []
    for c in second_level_cats:
        nums = Products.objects.filter(cat__in=categories_tree(c.id)).count()
        if nums != 0:
            setattr(c, 'prod_count', nums) 
            cats.append(c)

    cats_list = [] 
    if len(cats) == 0:
        if brand:
            qs = Products.objects.filter(cat=cats_tmp.id, brand=brand).distinct()
        else:
            qs = Products.objects.filter(cat=cats_tmp.id).distinct()
    else:
        for c in cats:
            cats_list.append(c.id)
        groups = Categories.objects.filter(parent_id__in=cats_list)
        for g in groups:
            cats_list.append(g.id) 
        if brand:
            qs = Products.objects.filter(cat__in=cats_list, brand=brand).distinct()
        else:
            qs = Products.objects.filter(cat__in=cats_list).distinct()

    sort = request.GET.get('sort', None)
    show = request.GET.get('show', None)
    if sort == '2':
        qs = qs.order_by('price')
    elif sort == '3':
        qs = qs.order_by('-price')
    else:
        qs = qs 

    pag = pag_def(show)
    
    brands = qs.values('brand').annotate(brand_count=Count('brand')) 
    h1 = cats_tmp.name
    try:
        p = Paginator(qs, pag)
        page = request.GET.get('page')
        objects = p.get_page(page)
    except:
        pass
    if request.GET.get('load_all') == 'all':
        objects = qs
    

    #Article founder starts here
    search_list = search_splitter(h1)
    articles = Blogs.objects.all()
    art_w_list = []
    for i, article in enumerate(articles):
        we = get_weight(article.text, search_list)
        if we > 0.02:
            art_w_list.append({ 'article': article, 'weight': we})
        if i > 10:
            break


    context = {
            'objects': objects,
            'cars': show_cars(),
            'categories': cats,
            'brands': brands,
            'title_h1': h1,
            'brand': brand,
            'bread1': bread1,
            'bread2': bread2,
            'bread3': bread3,
            'cat': cats_tmp,
            'articles': art_w_list,
            }
    
    return render(request, 'products/newparts.html', context)

#Detailed product view starts here

def detailed(request, pk):
    cats = Categories.objects.filter(parent_id=0)
    try:
        obj = get_object_or_404(Products, id=int(pk))
        bread_sub2 = Categories.objects.get(id=obj.cat.first().parent_id)
        bread_sub1 = Categories.objects.get(id=bread_sub2.parent_id)
    except Exception as e:
        raise Http404
    try:
        aver = Rating.objects.get(object_id=pk)
    except:
        aver = 0
    # Похожие товары
    similar_products = Products.objects.filter(cat=obj.cat.first().id)


    comments = Comment.objects.filter_by_instance(obj)
    comments = Comment.objects.filter_by_instance(obj)

    initial_data = {
        'content_type': obj.get_content_type,
        'object_id': obj.id,
    }

    form = CommentForm(request.POST or None, initial=initial_data)
    user_string = None
    if form.is_valid():

        if request.user.is_authenticated:
            user_string = request.user
        elif form.cleaned_data.get('user') is not None:
            user_string = form.cleaned_data.get('user')
        else:
            user_string = 'ANONIMUS'

        c_type = form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get('content')
        parent_obj = None
        try:
            parent_id = request.POST.get('parent_id')
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            content_type=content_type,
            object_id=obj_id,
            content=strip_tags(content_data),
            parent=parent_obj,
            user=strip_tags(user_string),
        )
        url = new_comment.content_object.get_absolute_url()
        send_mail(
                'Ducatoparts.ru новый комментарий',
                f'На дукато партс оставили новый комментарий на странице {url}',
                'angara99@gmail.com',
                ['angara99@gmail.com', 'yellkalolka@gmail.com'],
                fail_silently=False,
                )
        return HttpResponseRedirect(url)
    

    #comments count stuff
    def check_comment_count():
        count = comments.count() % 10
        comment_word = 'КОММЕНТАРИЕВ'
        if count == 1:
            comments_word = 'КОММЕНТАРИЙ'
        elif count > 1 and count < 5:
            comment_word = 'КОММЕНТАРИЯ'
        elif count >= 5:
            comment_word = 'КОММЕНТАРИЕВ'
        return comment_word
    # Форма звонка Вася

    e_form = EmailFormLight(request.POST or None)

    #Article founder starts here
    search_list = search_splitter(obj.name)
    articles = Blogs.objects.all()
    art_w_list = []
    for i, article in enumerate(articles):
        we = get_weight(article.text, search_list)
        if we > 0.02:
            art_w_list.append({ 'article': article, 'weight': we})
        if i > 10:
            break
    #Добавляем аналоги
    analogs = Products.objects.filter(cat_n=obj.cat_n).exclude(id=obj.id)
    if not analogs:
        analogs = None



    context = {
            'object': obj,
            'categories': cats,
            'cars': show_cars(),
            'comments': comments,
            'comment_count_word': check_comment_count(),
            'comment_form': form,
            'email_form': e_form,
            'bread_sub1': bread_sub1,
            'bread_sub2': bread_sub2,
            'similar_products': similar_products,
            'aver': aver,
            'articles': art_w_list,
            'analogs': analogs,

            }
    return render(request, 'products/product.html', context)


def search(request):
    #qs = Products.objects.filter(name__icontains="фильтр").distinct()

    sale_prod = settings.SALES_ON_SEARCH 
    brakes = Products.objects.filter(id__in=sale_prod)

    search = request.GET.get('search', None)
    search = strip_tags(search)
    search = search.strip(' ')

    def search_splitter(search):
        from .stemmer import Porter
        s = Porter()
        search_list = search.split(' ')
        new_search_list = []
        for word in search_list:
            try:
                n_w = s.stem(word)
            except:
                n_w = word
            new_search_list.append(n_w)
        return(new_search_list)

    cars_l = request.GET.getlist('car')
    cats_l = request.GET.getlist('cat')
    brands_l = request.GET.getlist('brand')
    tag = request.GET.get('tag')

    if search is None:
        qs_s = f'Products.objects.all().distinct().filter('
        if cars_l:
            qs_s += f'Q(car__in={cars_l}) & '
        if cats_l:
            qs_s += f'Q(cat__in={cats_l}) & '
        if brands_l:
            qs_s += f'Q(brand__in={brands_l}) & '
        else:
            pass
        qs_s = qs_s.rstrip()
        qs_s = qs_s.rstrip('&').rstrip()
        qs_s += ')[:100]'
        qs = eval(qs_s)        
    else:
        search_list = search_splitter(search)

        if len(search_list) == 1:
            qs_s = f'Products.objects.filter(Q(name__icontains="{search}") | Q(cat_n__icontains="{search}")).distinct().filter('
        else:
            qs_s = f'Products.objects.filter('
            for word in search_list:
                qs_s += f'Q(name__icontains="{word}") & '

        if cars_l:
            qs_s += f'Q(car__in={cars_l}) & '
        if cats_l:
            qs_s += f'Q(cat__in={cats_l}) & '
        if brands_l:
            qs_s += f'Q(brand__in={brands_l}) & '
        else:
            pass
        qs_s = qs_s.rstrip()
        qs_s = qs_s.rstrip('&').rstrip()
        qs_s += ')'
        qs = eval(qs_s)

    if tag:
        qs = qs.filter(name__icontains=tag)
    qs_cars = qs.values('car').annotate(scount=Count('car'))

    qs_brand = qs.values('brand').annotate(bcount=Count('brand'))

    qs_cats = qs.prefetch_related('cat')#.annotate(ccount=Count('cat'))
    l = []
    for q in qs_cats:
        for c in q.cat.all():
            caa = Categories.objects.get(id=c.parent_id)
            if caa.id not in l:
                l.append(caa.id)
    cats = Categories.objects.filter(parent_id__in=l)
    
    ca = [] 
    for c in cats:
        p = qs.filter(cat=c.id)
        if not p:
            continue
        ca.append({'cat': c, 'ccount': p.count()})
    sort = request.GET.get('sort', None)
    show = request.GET.get('show', None)
    if sort == '3':
        qs = qs.order_by('-price')
    elif sort == '2':
        qs = qs.order_by('price')
    else: 
        qs = qs.order_by('?')
    pag = pag_def(show)

    try:
        p = Paginator(qs, pag)
        page = request.GET.get('page')
        objects = p.get_page(page)
    except:
        pass
    if request.GET.get('load_all') == 'all':
        objects = qs
    
    # Обработка слов в нормальный падеж
    def words(count):
        if count:
            if count % 10 == 1:
                word = 'запчасть'
            elif (count % 10 >= 2 and count % 10 <=4) or (count >= 2 and count <= 4):
                word = 'запчасти'
            elif count % 10 > 4 or count > 4:
                word = 'запчастей'
            return word
        else:
            return None

    #Article founder starts here
    articles = Blogs.objects.all()
    art_w_list = []
    for i, article in enumerate(articles):
        we = get_weight(article.text, search_list)
        if we > 0.02:
            art_w_list.append({ 'article': article, 'weight': we})
        if i > 10:
            break

    
        
        

    
    context = {
                'tags': settings.TAGS_LIST,
                'objects': objects,
                'cars': qs_cars, 
                'search_categories': ca,
                'brands': qs_brand,
                'brakes': brakes,
                'total_items': p.count,
                'zapchasti_word': words(p.count),
                'articles': art_w_list,
            }
    return render(request, 'products/search.html', context)
