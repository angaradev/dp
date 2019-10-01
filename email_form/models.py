from django.db import models
from django.utils import timezone

# Create your models here.
class EmailModel(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    timestamp = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'обратный звонок'
        verbose_name_plural = 'обратные звонки'


    def __str__(self):
        return self.phone

