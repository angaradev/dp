from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from products.views import show_cars
from .models import Blogs, OldBlogs
from django.db.models import Count
from django.db.models.functions import TruncYear
from django.db.models import Q
from products.models import Categories
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from comments.models import Comment
from django.utils.html import strip_tags
from django.core.mail import send_mail

def blogs(request):
    req_cat = request.GET.get('category')
    
    if req_cat:
        qs = Blogs.objects.filter(category=req_cat)
    else: 
            qs = Blogs.objects.all()

    if request.GET.get('arch'):
        req_arch = request.GET.get('arch').split(' ')[0]
        qs = qs.filter(publish__year=req_arch)

    search_blog = request.GET.get('search_blog')
    if search_blog:
        qs = qs.filter( Q(title__icontains=search_blog) | Q(text__icontains=search_blog) )
    p = Paginator(qs, 6)
    page = request.GET.get('page')
    objects = p.get_page(page)
    resents = qs.order_by('-publish')[:4]
    archeves = qs.annotate(year=TruncYear('publish')).values('year').annotate(year_count=Count('id'))

    cats = qs.annotate(cat_count=Count('category'))
    context = {
            'categories': Categories.objects.filter(parent_id=0),
            'objects': objects,
            'cars': show_cars(),
            'categs': cats,
            'resents': resents,
            'archeves': archeves,

            }
    return render(request, 'blog/blogs.html', context)


def blog(request, slug):
    obj = get_object_or_404(Blogs, slug=slug)
    obj.number_views += 1
    obj.save()
    
    related = Blogs.objects.filter(category=obj.category).exclude(slug=slug)[:2]
    comments = Comment.objects.filter_by_instance(obj)
    if request.user.is_authenticated:
        value = str(request.user).upper()

        initial_data = {
                'content_type': obj.get_content_type,
                'object_id': obj.id,
                'user': value,
                
                }
    else:
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
            print(parent_id)
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()
                    
        new_comment, created = Comment.objects.get_or_create(
               content_type = content_type,
               object_id = obj_id,
               content = strip_tags(content_data),
               parent = parent_obj,
               user = strip_tags(user_string),
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


    context = {
            'categories': Categories.objects.filter(parent_id=0),
            'object': obj,
            'cars': show_cars(),
            'related': related,
            'comments': comments,
            'comment_count_word': check_comment_count(),
            'comment_form': form,
            }
    return render(request, 'blog/blog.html', context)



def oldblogs(request):
    req_cat = request.GET.get('category')
    
    if req_cat:
        
        qs = OldBlogs.objects.filter(category=req_cat)
    else: 
            qs = OldBlogs.objects.all()#filter(id__in=[1,2])

    if request.GET.get('arch'):
        req_arch = request.GET.get('arch').split(' ')[0]
        qs = qs.filter(publish__year=req_arch)

    search_blog = request.GET.get('search_blog')
    if search_blog:
        qs = qs.filter( Q(title__icontains=search_blog) | Q(text__icontains=search_blog) )
    p = Paginator(qs, 6)
    page = request.GET.get('page')
    objects = p.get_page(page)
    resents = qs.order_by('-publish')[:4]
    archeves = qs.annotate(year=TruncYear('publish')).values('year').annotate(year_count=Count('id'))

    cats = qs.annotate(cat_count=Count('category'))
    context = {
            'categories': Categories.objects.filter(parent_id=0),
            'objects': objects,
            'cars': show_cars(),
            'categs': cats,
            'resents': resents,
            'archeves': archeves,

            }
    return render(request, 'blog/blogs.html', context)

def oldblog(request, pk):
    obj = OldBlogs.objects.get(id=pk)
    obj.number_views += 1
    obj.save()
    
    related = OldBlogs.objects.filter(category=obj.category).exclude(id=pk)
    comments = Comment.objects.filter_by_instance(obj)
    if request.user.is_authenticated:
        value = str(request.user).upper()

        initial_data = {
                'content_type': obj.get_content_type,
                'object_id': obj.id,
                'user': value,
                
                }
    else:
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
            print(parent_id)
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()
                    
        new_comment, created = Comment.objects.get_or_create(
               content_type = content_type,
               object_id = obj_id,
               content = strip_tags(content_data),
               parent = parent_obj,
               user = strip_tags(user_string),
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


    context = {
            'categories': Categories.objects.filter(parent_id=0),
            'object': obj,
            'cars': show_cars(),
            'related': related,
            'comments': comments,
            'comment_count_word': check_comment_count(),
            'comment_form': form,
            }
    return render(request, 'blog/blog.html', context)



