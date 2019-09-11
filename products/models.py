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
    cat = models.ForeignKey(Categories, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    car = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50, null=True)
    cross = models.ManyToManyField(Cross, verbose_name="cross verbose name")
    price = models.FloatField(null=True, blank=True)
    condition = models.BooleanField(default=True)
    weight = models.FloatField(blank=True)
    color = models.CharField(max_length=20, blank=True)
    real_weight = models.FloatField(blank=True)



