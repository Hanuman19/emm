# Generated by Django 3.1.5 on 2021-04-05 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0029_auto_20210405_0414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result_trail',
            name='gp',
            field=models.IntegerField(default=0, verbose_name='Груженные вагоны'),
        ),
        migrations.AlterField(
            model_name='result_trail',
            name='pv',
            field=models.IntegerField(default=0, verbose_name='Порожние вагоны'),
        ),
        migrations.AlterField(
            model_name='result_trail',
            name='weight',
            field=models.IntegerField(default=0, verbose_name='Весс поезда'),
        ),
    ]
