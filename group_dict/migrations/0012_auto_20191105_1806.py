# Generated by Django 2.2.6 on 2019-11-05 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_dict', '0011_kerneltmp_group_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='kernelreadycommercial',
            name='group_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='kernelreadyinfo',
            name='group_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
