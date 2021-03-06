# Generated by Django 3.1.5 on 2021-04-14 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0031_auto_20210405_0431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result_manevr',
            name='dt_end',
        ),
        migrations.RemoveField(
            model_name='result_manevr',
            name='dt_start',
        ),
        migrations.RemoveField(
            model_name='result_manevr',
            name='fact',
        ),
        migrations.RemoveField(
            model_name='result_manevr',
            name='norm',
        ),
        migrations.RemoveField(
            model_name='result_manevr',
            name='saving',
        ),
        migrations.RemoveField(
            model_name='result_manevr',
            name='work_time',
        ),
        migrations.AddField(
            model_name='result_manevr',
            name='dtEndManevr',
            field=models.IntegerField(default=0, verbose_name='Дт на конец операции'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result_manevr',
            name='dtStartManevr',
            field=models.IntegerField(default=0, verbose_name='Дт на начало операции'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result_manevr',
            name='equipment',
            field=models.IntegerField(default=0, verbose_name='Экипировка'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result_manevr',
            name='fact_manevr',
            field=models.IntegerField(default=0, verbose_name='Фактический расход ДТ'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result_manevr',
            name='norm_manevr',
            field=models.DecimalField(decimal_places=1, max_digits=6, null=True, verbose_name='Нормированный расход ДТ'),
        ),
        migrations.AddField(
            model_name='result_manevr',
            name='obduv',
            field=models.BooleanField(blank=True, null=True, verbose_name='Обдув вагонов'),
        ),
        migrations.AddField(
            model_name='result_manevr',
            name='obrabotka',
            field=models.BooleanField(blank=True, null=True, verbose_name='Обработка вагонов'),
        ),
        migrations.AddField(
            model_name='result_manevr',
            name='prostoy',
            field=models.BooleanField(blank=True, null=True, verbose_name='Простой'),
        ),
        migrations.AddField(
            model_name='result_manevr',
            name='saving_manevr',
            field=models.DecimalField(decimal_places=1, max_digits=6, null=True, verbose_name='Экономия'),
        ),
        migrations.AddField(
            model_name='result_manevr',
            name='thrust',
            field=models.BooleanField(blank=True, null=True, verbose_name='Вытяжка'),
        ),
        migrations.AddField(
            model_name='result_manevr',
            name='work_time_manevr',
            field=models.IntegerField(default=0, verbose_name='Общее время работы'),
            preserve_default=False,
        ),
    ]
