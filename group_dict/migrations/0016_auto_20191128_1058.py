# Generated by Django 2.2.6 on 2019-11-28 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_dict', '0015_groups_old_group_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='full_minus',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='groups',
            name='full_plus',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='groups',
            name='inner_labels',
            field=models.CharField(default='generic', max_length=10),
        ),
        migrations.AlterField(
            model_name='groups',
            name='old_group_id',
            field=models.CharField(blank=True, default=0, max_length=100),
        ),
    ]
