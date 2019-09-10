from django.shortcuts import render

from .models import ArtCategory, Blogs

def blogs(request):
    qs = Blogs.objects.all()
    context = {'objects': qs}
    return render(request, 'blog/blogs.html', context)


