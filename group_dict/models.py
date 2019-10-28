from django.db import models
import csv


class Kernel(models.Model):
    
    keywords = models.CharField(max_length=500)
    freq    = models.PositiveIntegerField()
    chk = models.BooleanField(default=False)

    def __str__(self):
        return self.keywords
    
    def file_insert(self, path):
        i = 0
        with open(path) as f:
            reader = csv.reader(f)
            for row in reader:
                created = self.__class__.objects.get_or_create(
                        keywords = row[0],
                        freq = row[1],
                        )
                if created:
                    i += 1
        return i
   
class Nomenklatura(models.Model):

    name = models.CharField(max_length=500, blank=True, null=True)
    chk = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def file_insert(self, path):
        i = 0
        with open(path) as f:
            reader = csv.reader(f)
            for row in reader:
                created = self.__class__.objects.get_or_create(
                        name = row[0],
                        )
                if created:
                    i += 1
        return i

class Groups(models.Model):

    name = models.CharField(max_length=500, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE)
    plus = models.CharField(max_length=1000, blank=True)
    minus = models.CharField(max_length=1000, blank=True)
    
    def __str__(self):
        return self.name




    
