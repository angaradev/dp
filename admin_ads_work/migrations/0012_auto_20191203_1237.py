# Generated by Django 2.2.6 on 2019-12-03 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_ads_work', '0011_keywords_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keywords',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_ads_work.AdGroups'),
        ),
        migrations.AlterField(
            model_name='negative',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_ads_work.AdGroups'),
        ),
    ]
