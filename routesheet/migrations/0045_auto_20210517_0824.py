# Generated by Django 3.1.5 on 2021-05-17 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0044_auto_20210514_0416'),
    ]

    operations = [
        migrations.AddField(
            model_name='result_manevr',
            name='gp',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Груженные вагоны'),
        ),
        migrations.AddField(
            model_name='result_manevr',
            name='pv',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Порожние вагоны'),
        ),
    ]
