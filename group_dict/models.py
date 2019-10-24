from django.db import models


class Kernel(models.Model):
    
    keywords = models.CharField(max_length=500)
    freq    = models.PositiveIntegerField()
    





    
