# Generated by Django 3.1.5 on 2021-03-11 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0022_auto_20210311_0820'),
    ]

    operations = [
        migrations.AddField(
            model_name='result_trail',
            name='lokoNumber',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='routesheet.loko', verbose_name='№ секции'),
            preserve_default=False,
        ),
    ]