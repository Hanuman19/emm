# Generated by Django 3.1.5 on 2021-02-04 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0003_auto_20210204_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loko',
            name='region',
            field=models.ManyToManyField(to='routesheet.Region', verbose_name='Регион'),
        ),
    ]
