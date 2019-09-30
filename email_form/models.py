from django.db import models
import datetime

# Create your models here.
class EmailModel(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    timestamp = models.DateField(default=datetime.date.today())

    class Meta:
        verbose_name = 'обратный звонок'
        verbose_name_plural = 'обратные звонки'


    def __str__(self):
        return self.phone

