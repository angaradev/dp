from django.db import models, connection
import csv


class KernelTmp(models.Model):
    
    keywords = models.CharField(max_length=500, default='')
    freq    = models.PositiveIntegerField(default=0)
    chk = models.BooleanField(default=0)
    group_id = models.IntegerField(default=0)
    group_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.keywords


#Модель ядра очищенного от общих минус слов
class KernelCleanedFromTrash(models.Model):
    
    keywords = models.CharField(max_length=500)
    freq    = models.PositiveIntegerField()
    chk = models.BooleanField(default=False)

    def __str__(self):
        return self.keywords
    

#Модель для коммерческих запросов
class KernelReadyCommercial(models.Model):
    
    keywords = models.CharField(max_length=500)
    freq    = models.PositiveIntegerField()
    chk = models.BooleanField(default=False)
    group_id = models.IntegerField(default=0)
    group_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.keywords


#Модель для информационных запросов
class KernelReadyInfo(models.Model):
    
    keywords = models.CharField(max_length=500)
    freq    = models.PositiveIntegerField()
    chk = models.BooleanField(default=False)
    group_id = models.IntegerField(default=0)
    group_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.keywords
    

#Главная модель для самого первого шага и загрузки в базу
class Kernel(models.Model):
    
    keywords = models.CharField(max_length=500)
    freq    = models.PositiveIntegerField()
    chk = models.BooleanField(default=False)

    def __str__(self):
        return self.keywords
    
    def file_insert(self, path):
        cursor = connection.cursor()
        q = 'TRUNCATE TABLE ' + self._meta.db_table
        cursor.execute(q)

        with open(path, encoding='utf-8') as f:
            dialect = csv.Sniffer().sniff(f.read(1024))
            reader = csv.reader(f, dialect)
            l = []
            for x in reader:
                if not x[1]:
                    continue
                l.append(x)

        insert_q = "INSERT INTO " + self._meta.db_table + " (keywords, freq) VALUES (%s, %s)"
        i = cursor.executemany(insert_q, l)
        return i
   
class Nomenklatura(models.Model):

    name = models.CharField(max_length=500, blank=True, null=True)
    chk = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def file_insert(self, path):
        cursor = connection.cursor()
        q = 'TRUNCATE TABLE ' + self._meta.db_table
        cursor.execute(q)

        with open(path, encoding='utf-8') as f:
            dialect = csv.Sniffer().sniff(f.read(1024))
            reader = csv.reader(f, dialect)
            l = [[x[0]] for x in reader]

        insert_q = "INSERT INTO " + self._meta.db_table + " (name) VALUES (%s)"
        i = cursor.executemany(insert_q, l)
        return i

class Groups(models.Model):

    name = models.CharField(max_length=500, null=True, blank=True)
    parent = models.IntegerField()
    plus = models.CharField(max_length=1000, blank=True)
    minus = models.CharField(max_length=1000, blank=True)
    
    def __str__(self):
        return self.name

class CleanKernel(models.Model):
    minus = models.TextField(blank=True)


class InfoKernel(models.Model):
    minus = models.TextField(blank=True)




    
