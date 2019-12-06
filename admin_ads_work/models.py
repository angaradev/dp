from django.db import models
from group_dict.models import Groups



class Cars(models.Model):

    car_rus = models.CharField(max_length=100, null=True, blank=True)
    car_eng = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.car_rus

class Campaigns(models.Model):

    car = models.ForeignKey(Cars, on_delete=models.SET_NULL, null=True)
    camp_name = models.CharField(max_length=255, null=True, blank=True)
    fast_link_yand = models.CharField(max_length=66, null=True, blank=True)
    fast_link_yand_desc = models.CharField(max_length=126, null=True, blank=True)
    fast_link_yand_url = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.camp_name


class AdGroups(models.Model):
    
    group_id = models.ForeignKey(Groups, on_delete=models.SET_NULL, null=True)
    ad_group_name = models.CharField(max_length=255, blank=True)
    max_cpc     = models.DecimalField(blank=True, null=True, max_digits=7, decimal_places=2)
    max_cpm     = models.DecimalField(blank=True, null=True, max_digits=7, decimal_places=2)
    final_url   = models.CharField(max_length=500, blank=True)
    camp_id = models.ForeignKey(Campaigns, on_delete=models.SET_NULL, null=True)
    inner_labels = models.CharField(max_length=20, default='generic')
    chk = models.BooleanField(default=False)


class Adds(models.Model):

    AD_CHOICES = [
            ('one', 1),
            ('second', 2),
            ('third', 3)
            ]

    ad_group = models.ForeignKey(AdGroups, on_delete=models.CASCADE)
    headline1 = models.CharField(max_length=30, blank=True)
    path1 = models.CharField(max_length=15, blank=True)
    path2 = models.CharField(max_length=15, blank=True)
    headline2 = models.CharField(max_length=30, blank=True)
    headline3 = models.CharField(max_length=30, blank=True)
    description1 = models.CharField(max_length=90, blank=True)
    description2 = models.CharField(max_length=90, blank=True)
    description3 = models.CharField(max_length=90, blank=True)
    variant = models.CharField(max_length=20, choices=AD_CHOICES, default='one')
    camp_id = models.ForeignKey(Campaigns, on_delete=models.SET_NULL, null=True)
    

class AddsTemplate(models.Model):

    AD_CHOICES = [
            ('one', 1),
            ('second', 2),
            ('third', 3)
            ]

    camaign = models.ForeignKey(Campaigns, on_delete=models.CASCADE)
    headline1 = models.CharField(max_length=30, blank=True)
    headline2 = models.CharField(max_length=30, blank=True)
    headline3 = models.CharField(max_length=30, blank=True)
    description1 = models.CharField(max_length=90, blank=True)
    description2 = models.CharField(max_length=90, blank=True)
    description3 = models.CharField(max_length=90, blank=True)
    path1 = models.CharField(max_length=15, blank=True)
    path2 = models.CharField(max_length=15, blank=True)
    variant = models.CharField(max_length=20, choices=AD_CHOICES, default='one')

class Keywords(models.Model):

    keyword = models.CharField(max_length=255, null=True)
    group     = models.ForeignKey(AdGroups, on_delete=models.SET_NULL, null=True)
    labels      = models.CharField(max_length=255, blank=True)
    criterion_type = models.CharField(max_length=20, null=True, blank=True)


class Negative(models.Model):

    negative = models.CharField(max_length=255, null=True)
    group     = models.ForeignKey(AdGroups, on_delete=models.SET_NULL, null=True)
