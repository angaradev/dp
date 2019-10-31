# Generated by Django 2.2.6 on 2019-10-29 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_dict', '0006_kerneltmp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kerneltmp',
            name='freq',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='kerneltmp',
            name='keywords',
            field=models.CharField(default='', max_length=500),
        ),
    ]