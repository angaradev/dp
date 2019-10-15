from django.contrib import admin
from .models import EmailModel

class EmailAdmin(admin.ModelAdmin):
    class Meta:
        model = EmailModel
        verbose_name_plural = 'Обратные Звонки'


admin.site.register(EmailModel)
