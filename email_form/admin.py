from django.contrib import admin
from .models import EmailModel

class EmailAdmin(admin.ModelAdmin):
    class Meta:
        model = EmailModel


admin.site.register(EmailModel)
