from django.db import models
import datetime




class PhotoStatistic(models.Model):

    checked_count    = models.IntegerField(default=0)
    unchecked_count    = models.IntegerField(default=0)
    checked_date = models.DateField(default=datetime.date.today, unique=True)
