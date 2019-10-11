from django.db import models

class RedireCtcat(models.Model):
    id_old = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=70, blank=True, null=True)
    id_new = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'redirect_cat'



class RedirectProductOldToNew(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    id_new = models.IntegerField(blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'redirect_product_old_to_new'
    

class RedirectProductOldToNewDictionary(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    id_new = models.IntegerField(blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'redirect_product_old_to_new_dictionary'
