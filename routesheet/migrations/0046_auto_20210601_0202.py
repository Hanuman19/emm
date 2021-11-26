# Generated by Django 3.1.5 on 2021-06-01 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0045_auto_20210517_0824'),
    ]

    operations = [
        migrations.AddField(
            model_name='result_trail',
            name='DoubleLokoNumber',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='number_loko_double', to='routesheet.loko', verbose_name='Номер 2-й секции'),
        ),
        migrations.AddField(
            model_name='result_trail',
            name='DoubleLokoType',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type_loko_double', to='routesheet.loko', verbose_name='Тип 2-й секции'),
        ),
        migrations.AddField(
            model_name='result_trail',
            name='doublePull',
            field=models.BooleanField(blank=True, null=True, verbose_name='Двойная тяга'),
        ),
    ]
