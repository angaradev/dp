from django.db import models
from group_dict.models import Groups



class AdGroups(models.Model):
    
    group_id = models.ForeignKey(Groups, on_delete=models.SET_NULL, null=True)
    ad_group_name = models.CharField(max_length=255, blank=True)
    labels      = models.CharField(max_length=255, blank=True)
    max_cpc     = models.DecimalField(blank=True, max_digits=7, decimal_places=2)
    max_cpm     = models.DecimalField(blank=True, max_digits=7, decimal_places=2)
    final_url   = models.CharField(max_length=500, blank=True)
    critarion_type = models.CharField(max_length=100, blank=True)
    description1 = models.CharField(max_length=90, blank=True)
    description2 = models.CharField(max_length=90, blank=True)
    description3 = models.CharField(max_length=90, blank=True)
    headline1 = models.CharField(max_length=30, blank=True)
    headline2 = models.CharField(max_length=30, blank=True)
    headline3 = models.CharField(max_length=30, blank=True)
    path1 = models.CharField(max_length=15, blank=True)
    path2 = models.CharField(max_length=15, blank=True)


class Keywords(models.Model):

    keyword = models.CharField(max_length=255, null=True)
    group     = models.ForeignKey(AdGroups, on_delete=models.SET_NULL, null=True)



class Negative(models.Model):

    negative = models.CharField(max_length=255, null=True)
    group     = models.ForeignKey(AdGroups, on_delete=models.SET_NULL, null=True)
