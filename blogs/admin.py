from django.contrib import admin

from .models import Blogs


class BlogsAdmin(admin.ModelAdmin):

    class Meta:
        model = Blogs


admin.site.register(Blogs)


