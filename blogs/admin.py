from django.contrib import admin

from .models import Blogs, ArtCategory


class BlogsAdmin(admin.ModelAdmin):

    class Meta:
        model = Blogs


admin.site.register(Blogs)
admin.site.register(ArtCategory)


