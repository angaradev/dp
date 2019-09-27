from django.db import models

# Create your models here.
class EmailModel(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.phone

