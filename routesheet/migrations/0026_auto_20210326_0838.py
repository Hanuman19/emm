# Generated by Django 3.1.5 on 2021-03-26 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0025_auto_20210326_0723'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='lokoNumber',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lokoNumber', to='routesheet.loko', verbose_name='Тип секции'),
        ),
        migrations.AlterField(
            model_name='report',
            name='fact_manevr',
            field=models.IntegerField(blank=True, null=True, verbose_name='Фактический расход ДТ'),
        ),
        migrations.AlterField(
            model_name='report',
            name='fact_result',
            field=models.IntegerField(blank=True, null=True, verbose_name='Фактический расход ДТ'),
        ),
        migrations.AlterField(
            model_name='report',
            name='fact_trail',
            field=models.IntegerField(blank=True, null=True, verbose_name='Фактический расход ДТ'),
        ),
        migrations.AlterField(
            model_name='report',
            name='typeLoko',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='typeLoko', to='routesheet.loko', verbose_name='Тип секции'),
        ),
        migrations.AlterField(
            model_name='report',
            name='work_time_manevr',
            field=models.IntegerField(blank=True, null=True, verbose_name='Общее время работы'),
        ),
        migrations.AlterField(
            model_name='report',
            name='work_time_trail',
            field=models.IntegerField(blank=True, null=True, verbose_name='Общее время работы'),
        ),
    ]
