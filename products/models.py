from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=100, null=True)
    parent_id = models.IntegerField(null=True)
    slug = models.CharField(max_length=500, blank=True, null=True)
    class Meta:
        verbose_name_plural = "Категории"


class Cross(models.Model):
    orig_n = models.CharField(max_length=50)
    oem_n = models.CharField(max_length=50)


class Products(models.Model):
    cat = models.ManyToManyField(Categories)
    name = models.CharField(max_length=255, null=True)
    cat_n = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=100, null=True)
    car = models.CharField(max_length=255, null=True)
    car_model = models.CharField(max_length=50, null=True)
    cross = models.ManyToManyField(Cross, verbose_name="cross verbose name")
    price = models.FloatField(null=True, blank=True)
    cond = models.BooleanField(default=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    real_weight = models.FloatField(blank=True, null=True)
    seller = models.CharField(max_length=100, blank=True, null=True)



