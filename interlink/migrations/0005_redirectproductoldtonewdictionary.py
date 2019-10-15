# Generated by Django 2.2.6 on 2019-10-10 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interlink', '0004_delete_redirectproductoldtonewdictionary'),
    ]

    operations = [
        migrations.CreateModel(
            name='RedirectProductOldToNewDictionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('id_new', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'redirect_product_old_to_new_dictionary',
                'managed': True,
            },
        ),
    ]
