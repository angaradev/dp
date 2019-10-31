# Generated by Django 2.2.6 on 2019-10-31 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_dict', '0008_kerneltmp_group_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='KernelCleanedFromTrash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords', models.CharField(max_length=500)),
                ('freq', models.PositiveIntegerField()),
                ('chk', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='KernelReadyCommercial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords', models.CharField(max_length=500)),
                ('freq', models.PositiveIntegerField()),
                ('chk', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='KernelReadyInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords', models.CharField(max_length=500)),
                ('freq', models.PositiveIntegerField()),
                ('chk', models.BooleanField(default=False)),
            ],
        ),
    ]