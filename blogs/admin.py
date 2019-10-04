from django.contrib import admin

from .models import Blogs, OldBlogs


class BlogsAdmin(admin.ModelAdmin):

    class Meta:
        model = Blogs


admin.site.register(Blogs)
admin.site.register(OldBlogs)


