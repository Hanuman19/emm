# Generated by Django 3.1.5 on 2021-02-01 01:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='driver_area', to='routesheet.region', verbose_name='Участок'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='driver_region', to='routesheet.region', verbose_name='Регион'),
        ),
    ]
