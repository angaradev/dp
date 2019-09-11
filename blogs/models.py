from django.db import models
import os
import random


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    new_filename = random.randint(1, 234982304)
    final_filename = '{}{}'.format(new_filename, ext)
    return f'blog/{new_filename}/{final_filename}'


class ArtCategory(models.Model):
    name = models.CharField(max_length=100)


class Blogs(models.Model):
    cat = models.ForeignKey(ArtCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    published = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

