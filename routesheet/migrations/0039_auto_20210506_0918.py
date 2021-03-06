# Generated by Django 3.1.5 on 2021-05-06 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0038_auto_20210430_0622'),
    ]

    operations = [
        migrations.AddField(
            model_name='result_manevr',
            name='station',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='stationManevr', to='routesheet.region', verbose_name='Станция'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='result_trail',
            name='stationArr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stationArr', to='routesheet.region', verbose_name='Станция прибытия'),
        ),
        migrations.AlterField(
            model_name='result_trail',
            name='stationDep',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stationDep', to='routesheet.region', verbose_name='Станция отправления'),
        ),
    ]
