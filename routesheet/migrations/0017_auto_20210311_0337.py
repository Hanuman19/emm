# Generated by Django 3.1.5 on 2021-03-11 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0016_auto_20210303_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='result_trail',
            name='station_arr',
            field=models.CharField(default=1, max_length=50, verbose_name='Станция прибытия'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result_trail',
            name='station_dep',
            field=models.CharField(default='test', max_length=50, verbose_name='Станция отправления'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='settings',
            name='settings',
            field=models.TextField(blank=True, null=True, verbose_name='Настройки'),
        ),
    ]
