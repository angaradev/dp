from django.db import models

# Create your models here.
class Tableredirectcat(models.Model):
    id_old = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=70, blank=True, null=True)
    id_new = models.IntegerField(blank=True, null=True)

    class meta:
        managed = False
        db_table = 'table_redirect_cat'
