from django.db import models

class Tableredirectcat(models.Model):
    id_old = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=70, blank=True, null=True)
    id_new = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'table_redirect_cat'



#class SubcatRedirect(models.Model):
#    old_id = models.IntegerField(blank=True, null=True)
#    new_id = models.IntegerField(blank=True, null=True)
#    name = models.CharField(max_length=255, null=True, blank=True)
    
    
